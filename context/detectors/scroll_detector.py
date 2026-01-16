# detectors/scroll_detector.py
import asyncio
import json
import websockets
import threading
import time
from typing import Dict, Optional

class ScrollDetector:
    def __init__(self,
                 velocity_thresholds: Optional[Dict[str, float]] = None,
                 frequency_thresholds: Optional[Dict[str, float]] = None,
                 max_events: int = 25):
        self.velocity_thresholds = velocity_thresholds or {'slow': 80, 'fast': 800}
        self.frequency_thresholds = frequency_thresholds or {'slow': 0.8, 'fast': 6.0}
        self.max_events = max_events
        self.events = []  # [{position, timestamp}]
        self.last_type = "normal"
        self._lock = threading.Lock()
        self._running = False
        self._thread = None

    def add_scroll_event(self, position: float, timestamp: Optional[float] = None):
        ts = timestamp or time.time()
        with self._lock:
            self.events.append({'position': position, 'timestamp': ts})
            if len(self.events) > self.max_events:
                self.events.pop(0)

    def get_scroll_type(self) -> str:
        with self._lock:
            if len(self.events) < 3:
                return "normal"
            velocities = []
            time_diffs = []
            for i in range(1, len(self.events)):
                pos_diff = abs(self.events[i]['position'] - self.events[i-1]['position'])
                dt = self.events[i]['timestamp'] - self.events[i-1]['timestamp']
                if dt < 0.001:
                    continue
                velocities.append(pos_diff / dt)
                time_diffs.append(dt)
            if not velocities:
                return "normal"
            avg_velocity = sum(velocities) / len(velocities)
            avg_interval = sum(time_diffs) / len(time_diffs)
            avg_frequency = 1 / avg_interval if avg_interval > 0 else 0

            if avg_velocity > self.velocity_thresholds['fast'] or avg_frequency > self.frequency_thresholds['fast']:
                self.last_type = "fast_scroller"
            elif avg_velocity < self.velocity_thresholds['slow'] or avg_frequency < self.frequency_thresholds['slow']:
                self.last_type = "slow_scroller"
            else:
                self.last_type = "normal"
            return self.last_type

    def detect_scroll(self) -> str:  # ← Add this alias so context_manager.py can call it
        return self.get_scroll_type()

    def _ws_loop(self):
        """Run the asyncio WebSocket server in a separate thread"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def scroll_handler(websocket):
            async for message in websocket:
                try:
                    data = json.loads(message)
                    if data.get("type") == "scroll":
                        y = data.get("scrollY", 0)
                        self.add_scroll_event(y)
                        scroll_type = self.get_scroll_type()
                        await websocket.send(json.dumps({"type": "status", "scroll_type": scroll_type}))
                except Exception as e:
                    print(f"WS error: {e}")

        async def main():
            server = await websockets.serve(scroll_handler, "127.0.0.1", 8765)
            print("ScrollDetector WebSocket running on ws://127.0.0.1:8765")
            await server.wait_closed()

        loop.run_until_complete(main())

    def start(self):
        if not self._running:
            self._running = True
            self._thread = threading.Thread(target=self._ws_loop, daemon=True)
            self._thread.start()
            print("ScrollDetector started (WebSocket listening)")

    def stop(self):
        self._running = False
        # Note: Graceful WS shutdown is tricky in thread; for demo we just let daemon thread die
        if self._thread:
            # Give some time to finish
            time.sleep(0.5)
        print("ScrollDetector stopped")