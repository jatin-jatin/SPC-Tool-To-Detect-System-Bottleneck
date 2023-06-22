# SPS: Sys_Perf_Check 
## Description
* **SPS** is a tool used to **diagnose and detect bottelneck components** in the **backend server stack**.
* It generates **varying load** to **test the server stack** and then **extract the generated logs** for creating **graphs for analysis**.
* These **graphs** can be **used to detect the bottleneck**.
* It consists of mainly two components [Client_end_script](https://github.com/jatin-jatin/SPS-Tool-To-Detect-System-Bottleneck/tree/main/client_end_script) and [server_end_script](https://github.com/jatin-jatin/SPS-Tool-To-Detect-System-Bottleneck/tree/main/server_end_script).
* **client_end_script** is **responsible** for **performance testing** and **displaying the graphs for analysis**. 
* **server_end_script** is **responsible** for **extracting and transferring the logs to client_end_script**.
### SPS Working
![SPC Working](https://github.com/jatin-jatin/SPS-Tool-To-Detect-System-Bottleneck/blob/main/pictures/SPC_Design.png)


## Example Usage

### Consider the following Architecture
![Server Architecture](https://github.com/jatin-jatin/SPS-Tool-To-Detect-System-Bottleneck/blob/main/pictures/architecture-new.png)
* Outer-nginx : Nginx Layer which hosts multiple other application as well.
* Inner-nginx : contains configuration settings for load balancing traffic .
* uWSGI : web server gateway interface defined used by python frameworks for running web apps
* Django : Backend framework, core app logic is written.

### Steps in Using SPC

#### 1. Register the sys_perf_check web end point
* The **web end point** should have the following url structure **https://host.com/sys_perf_check/<test-id>/users/**
* It should run for a bounded time we have kept in 10ms but it is configurable. Refer [sample](https://github.com/jatin-jatin/SPS-Tool-To-Detect-System-Bottleneck/blob/main/register_end_point/end_point_implementation.py) in python
![Register End point](https://github.com/jatin-jatin/SPS-Tool-To-Detect-System-Bottleneck/blob/main/pictures/endpoint.png)

#### 2. Run the **[server_end_script](https://github.com/jatin-jatin/SPS-Tool-To-Detect-System-Bottleneck/blob/main/server_end_script/server_end_script.py)**
* It requires a **components.json** file that contains the location of component logs. Refer [sample](https://github.com/jatin-jatin/SPS-Tool-To-Detect-System-Bottleneck/blob/main/server_end_script/components.json)
* Run this in the machine where you have hosted the server being tested.
* To run ```$ python3 server_end_script.py```

#### 3. Run the **[client_end_script](https://github.com/jatin-jatin/SPS-Tool-To-Detect-System-Bottleneck/blob/main/client_end_script/client_end_script.py)**
* It also requires the same **components.json** file
* **Run this in a separate machine** from the host being tested to make the testing uniform.
* configure the **ip of log host and server host.**
* To run ```$ python3 client_end_script.py -l <lower-bound> -u <upper-bound> -s <step-size> -t <time>```
![client_end](https://github.com/jatin-jatin/SPS-Tool-To-Detect-System-Bottleneck/blob/main/pictures/client_end.png)
<!-- **IMG** -->

### Result
* We tried two configurations of **uwsgi**. 
* One where it is poorly configured and other where it is properly configured.
![uWSGI configurations](https://github.com/jatin-jatin/SPS-Tool-To-Detect-System-Bottleneck/blob/main/pictures/uwsgi_config.png)
<!-- **IMG** -->
#### 1. Poorly Configured 
* In order to poorly configure uwsgi. We set number of processes in uwsgi to 5.
* The ideal configuration is 2*number of cores.
* The machine where we tested had 12 cores.
* The wide gap between component performance indicate 
![uWSGI poorly configured](https://github.com/jatin-jatin/SPS-Tool-To-Detect-System-Bottleneck/blob/main/pictures/poor_config.png)

#### 2. Well Configured 
* In order to properly configure uwsgi. We set number of processes in uwsgi to 24.
![uWSGI correctly configured](https://github.com/jatin-jatin/SPS-Tool-To-Detect-System-Bottleneck/blob/main/pictures/proper_config.png)

## Conclusion
* SPC allow us to diagnose backend stack bottleneck component.
* Also it can be used to fine tune application by modifying the end point implementation.
* For more details you can refer the report and presentation.
