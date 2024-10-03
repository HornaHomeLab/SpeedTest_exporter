from prometheus_client import Info, Gauge
from src.Prometheus.Registry import exporter_registry
from src.Model.SpeedTest import SpeedTest
from src.Model.SpeedTestSubModels.Ping import NoWorkloadPing, TransferPing
from src.Model.SpeedTestSubModels.Transfer import Transfer
from src.Model.SpeedTestSubModels.Interface import Interface
from src.Model.SpeedTestSubModels.Server import Server
from src.Model.SpeedTestSubModels.Result import Result
from src.Observability import *

tracer = trace.get_tracer("Prometheus/SpeedTestMetrics")


class SpeedTestMetrics:

    __ping_no_workload_jitter = Gauge(
        'ping_no_workload_jitter', 'Jitter of ping test with no workload, representing the variability in ping response times (measured in ms).',
        registry=exporter_registry
    )
    __ping_no_workload_latency = Gauge(
        'ping_no_workload_latency', 'Latency of ping test with no workload, indicating the round-trip time for data to reach the server and back (measured in ms).',
        registry=exporter_registry
    )
    __ping_no_workload_low = Gauge(
        'ping_no_workload_low', 'Lowest ping recorded during the no-workload test (measured in ms).',
        registry=exporter_registry
    )
    __ping_no_workload_high = Gauge(
        'ping_no_workload_high', 'Highest ping recorded during the no-workload test (measured in ms).',
        registry=exporter_registry
    )

    __packet_loss = Gauge(
        'packet_loss', 'Percentage of packets lost during the test, representing network reliability (scale 0.0 - 1.0).',
        registry=exporter_registry
    )

    __download_bandwidth = Gauge(
        'download_bandwidth', 'Measured download bandwidth (in bits per second).',
        registry=exporter_registry
    )
    __download_bytes = Gauge(
        'download_bytes', 'Total number of bytes downloaded during the test.',
        registry=exporter_registry
    )
    __download_elapsed = Gauge(
        'download_elapsed', 'Total time taken to complete the download test (measured in ms).',
        registry=exporter_registry
    )
    __download_latency_iqm = Gauge(
        'download_latency_iqm', 'Interquartile mean latency for download, representing a robust average latency measurement (measured in ms).',
        registry=exporter_registry
    )
    __download_latency_low = Gauge(
        'download_latency_low', 'Lowest latency recorded during the download test (measured in ms).',
        registry=exporter_registry
    )
    __download_latency_high = Gauge(
        'download_latency_high', 'Highest latency recorded during the download test (measured in ms).',
        registry=exporter_registry
    )
    __download_latency_jitter = Gauge(
        'download_latency_jitter', 'Jitter of latency during the download test, representing variability in download latency (measured in ms).',
        registry=exporter_registry
    )

    __upload_bandwidth = Gauge(
        'upload_bandwidth', 'Measured upload bandwidth (in bits per second).',
        registry=exporter_registry
    )
    __upload_bytes = Gauge(
        'upload_bytes', 'Total number of bytes uploaded during the test.',
        registry=exporter_registry
    )
    __upload_elapsed = Gauge(
        'upload_elapsed', 'Total time taken to complete the upload test (measured in ms).',
        registry=exporter_registry
    )
    __upload_latency_iqm = Gauge(
        'upload_latency_iqm', 'Interquartile mean latency for upload, representing a robust average latency measurement (measured in ms).',
        registry=exporter_registry
    )
    __upload_latency_low = Gauge(
        'upload_latency_low', 'Lowest latency recorded during the upload test (measured in ms).',
        registry=exporter_registry
    )
    __upload_latency_high = Gauge(
        'upload_latency_high', 'Highest latency recorded during the upload test (measured in ms).',
        registry=exporter_registry
    )
    __upload_latency_jitter = Gauge(
        'upload_latency_jitter', 'Jitter of latency during the upload test, representing variability in upload latency (measured in ms).',
        registry=exporter_registry
    )

    __isp = Info(
        'isp', 'Internet Service Provider (ISP) details.',
        registry=exporter_registry
    )
    __interface = Info(
        'interface_details', 'Details of the network interface used for the speed test.',
        registry=exporter_registry
    )
    __server = Info(
        'server_details', 'Details of the destination server used for the speed test (e.g., server location, IP address).',
        registry=exporter_registry
    )
    __result = Info(
        'result_details', 'Details of the SpeedTest result, including test ID, URL.',
        registry=exporter_registry
    )

    @staticmethod
    @tracer.start_as_current_span("SpeedTestMetrics.update_metrics")
    def update_metrics(test: SpeedTest):
        get_current_span()
        
        with tracer.start_as_current_span("update_ping_metrics"):
            SpeedTestMetrics.__update_ping_metrics(test.ping)
            
        with tracer.start_as_current_span("update_bandwidth_metrics"):
            SpeedTestMetrics.__update_download_metrics(test.download)
            SpeedTestMetrics.__update_upload_metrics(test.upload)
            
        with tracer.start_as_current_span("update_packet_loss_metrics"):
            SpeedTestMetrics.__update_packet_loss_and_isp(test.packet_loss, test.isp)
            
        with tracer.start_as_current_span("update_test_details_metrics"):
            SpeedTestMetrics.__update_interface(test.interface)
            SpeedTestMetrics.__update_server(test.server)
            SpeedTestMetrics.__update_result(test.result)
        
        logger.info(
            "SpeedTest metrics updated"
        )
        
        set_current_span_status()

    @staticmethod
    def __update_ping_metrics(obj: NoWorkloadPing):
        SpeedTestMetrics.__ping_no_workload_jitter.set(obj.jitter)
        SpeedTestMetrics.__ping_no_workload_latency.set(obj.latency)
        SpeedTestMetrics.__ping_no_workload_low.set(obj.low)
        SpeedTestMetrics.__ping_no_workload_high.set(obj.high)

    @staticmethod
    def __update_download_metrics(obj: Transfer):
        SpeedTestMetrics.__download_bandwidth.set(obj.bandwidth)
        SpeedTestMetrics.__download_bytes.set(obj.bytes)
        SpeedTestMetrics.__download_elapsed.set(obj.elapsed)

        SpeedTestMetrics.__update_download_ping(obj.latency)

    @staticmethod
    def __update_download_ping(obj: TransferPing):
        SpeedTestMetrics.__download_latency_iqm.set(obj.iqm)
        SpeedTestMetrics.__download_latency_low.set(obj.low)
        SpeedTestMetrics.__download_latency_high.set(obj.high)
        SpeedTestMetrics.__download_latency_jitter.set(obj.jitter)

    @staticmethod
    def __update_upload_metrics(obj: Transfer):
        SpeedTestMetrics.__upload_bandwidth.set(obj.bandwidth)
        SpeedTestMetrics.__upload_bytes.set(obj.bytes)
        SpeedTestMetrics.__upload_elapsed.set(obj.elapsed)

        SpeedTestMetrics.__update_upload_ping(obj.latency)

    @staticmethod
    def __update_upload_ping(obj: TransferPing):
        SpeedTestMetrics.__upload_latency_iqm.set(obj.iqm)
        SpeedTestMetrics.__upload_latency_low.set(obj.low)
        SpeedTestMetrics.__upload_latency_high.set(obj.high)
        SpeedTestMetrics.__upload_latency_jitter.set(obj.jitter)

    @staticmethod
    def __update_packet_loss_and_isp(packet_loss: float, isp: str):
        SpeedTestMetrics.__packet_loss.set(packet_loss)
        SpeedTestMetrics.__isp.info({"Name": isp})

    @staticmethod
    def __update_interface(obj: Interface):
        SpeedTestMetrics.__interface.info(obj.model_dump())

    @staticmethod
    def __update_server(obj: Server):
        SpeedTestMetrics.__server.info(obj.model_dump())

    @staticmethod
    def __update_result(obj: SpeedTest):
        SpeedTestMetrics.__result.info(obj.model_dump())
