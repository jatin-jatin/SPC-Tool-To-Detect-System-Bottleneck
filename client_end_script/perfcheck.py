from locust import HttpUser,SequentialTaskSet,task,constant,events
from locust.exception import StopUser
from client_end_script_helper import test_host,read_config

test_id,num_user=read_config()
url = "sys_perf_check/"+test_id+"/"+num_user+"/"
class PerfCheck(SequentialTaskSet):

    @task
    def perf_check(self):
        print(url)
        # with self.client.get(url,name="perf_check",catch_response=True,verify=False) as response:
        with self.client.get(url,name="perf_check",catch_response=True,verify=False) as response:
            print("perf_check:",response.text)

    # @task
    # def on_stop(self):
    #     raise StopUser()


class MySeqTest(HttpUser):
    # fixed_count=1
    wait_time=constant(1)
    host =test_host
    tasks = [PerfCheck]

