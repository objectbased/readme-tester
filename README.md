

## Syslog-ng Port Tracker
| source    |port | protocol   | path                                                                     | origin                                                                                                  |
|:----------|-------:|:-----------|:-------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------|
| cisco_asa |  10516 | udp,tcp    | /var/log/forward/cisco_asa/${HOST}/cisco_asa_${YEAR}-${MONTH}-${DAY}.log | [Link](https://github.com/objectbased/readme-tester/blob/main/syslog-ng/conf.d/integrations/cisco.conf) |
| palo_alto |  10617 | tcp        | /var/log/forward/palo_alto/${HOST}/palo_alto_${YEAR}-${MONTH}-${DAY}.log | [Link](https://github.com/objectbased/readme-tester/blob/main/syslog-ng/conf.d/integrations/palo.conf)  |