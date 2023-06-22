# SPS: Sys_Perf_Check 
## Description
* **SPS** is a tool used to diagnose and detect bottelneck components in the backend server stack.
* It generates **varying load** to **test the server stack** and then **extract the generated logs** for creating **graphs for analysis**.
* These **graphs** can be **used to detect the bottleneck**.
* It consists of mainly two components [Client_end_script](https://github.com/jatin-jatin/SPS-Tool-To-Detect-System-Bottleneck/tree/main/client_end_script) and [server_end_script](https://github.com/jatin-jatin/SPS-Tool-To-Detect-System-Bottleneck/tree/main/server_end_script).
* **client_end_script** is **responsible** for **performance testing** and **displaying the graphs for analysis**. 
* **server_end_script** is **responsible** for **extracting and transferring the logs to client_end_script**.
### SPS Working
![SPC Working](https://github.com/jatin-jatin/SPS-Tool-To-Detect-System-Bottleneck/blob/main/pictures/SPC_Design.png)


## Example Usage

### Consided the following Architecture