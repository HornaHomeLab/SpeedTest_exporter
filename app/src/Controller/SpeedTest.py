import src.Model as Model
import src.Utils as Utils

class SpeedTest:
    
    def check_components():
        Utils.SpeedTestByOokla.check_if_speedtest_package_exist()
    
    def perform_speed_test() -> Model.SpeedTest:
        test: Model.SpeedTest = Utils.SpeedTestByOokla.run_speedtest()
        Utils.PrometheusMetrics.update_metrics(test)
        return test
