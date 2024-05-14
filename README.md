# TikTok-Webhook
Sends new uploads of TikTok accounts to webhook

Args:

--webhook
Your Discord webhook. (Required)
 
--token
Your ms_token from TikTok cookies. (Required)

--account
Name of the accounts to monitor (Required)
        
--continuous
Continually check feed(s) based on --interval value. The default --interval is 1 hour.
        
--interval
Specify the wait interval in days, hours, minutes, and seconds (e.g., 1d2h30m)

--archive
Archive file to store previous feed(s) items. Default is feeds.txt located in the current working directory (cwd).

--force-old
Send webhook notifications when --archive file is empty.
