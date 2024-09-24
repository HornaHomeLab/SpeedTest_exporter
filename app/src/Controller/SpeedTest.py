import src.Model as Model
from src.Prometheus.SpeedTestMetrics import SpeedTestMetrics
import src.Utils as Utils

class SpeedTest:
    
    def check_components():
        Utils.SpeedTestByOokla.check_if_speedtest_package_exist()
    
    def perform_speed_test() -> Model.SpeedTest:
        test: Model.SpeedTest = Utils.SpeedTestByOokla.run_speedtest()
        SpeedTestMetrics.update_metrics(test)
        return test
