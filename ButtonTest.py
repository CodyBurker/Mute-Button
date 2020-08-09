import getZoomStatus as getZoomStatus
if getZoomStatus.DetectZoomMeeting() == True:
    # Zoom Meeting in Progress
    status = getZoomStatus.GetZoomStatus(toggleMute=True)
else:
    status = "zoomStatus:closed,zoomMute:disabled,zoomVideo:disabled,zoomShare:disabled"
print(status)


# ## NEed to run powershell to be fasterer
# $wshell = New-Object -ComObject wscript.shell;
#  $wshell.SendKeys('^%+') 
#   $wshell.SendKeys('+A')

# Idea in powershell:
# Powershell script checks zoom status
# Sends to arduion
# Reads arduino script
# 