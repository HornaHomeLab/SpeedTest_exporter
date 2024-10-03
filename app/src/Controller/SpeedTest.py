import src.Model as Model
from src.Prometheus.SpeedTestMetrics import SpeedTestMetrics
from src.Observability import *
import src.Utils as Utils

tracer = trace.get_tracer("Controller/SpeedTest")


class SpeedTest:

    def check_components():
        Utils.SpeedTestByOokla.check_if_speedtest_package_exist()

    @tracer.start_as_current_span("SpeedTest.perform_speed_test")
    def perform_speed_test() -> Model.SpeedTest:
        get_current_span()
        
        test: Model.SpeedTest = Utils.SpeedTestByOokla.run_speedtest()
        SpeedTestMetrics.update_metrics(test)
        
        set_current_span_status()
        return test
