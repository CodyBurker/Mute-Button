# Plan:
# Outer script to communicate with arduino every .1 seconds and check for button press, then update zoom.
# Innser script (job) to asynchronosly check zoom every second via python getZoomStatus.py
# Outer script will check for data from inner script, and if there is new data it will change button.

function toggleMute {

    $wshell = New-Object -ComObject wscript.shell;
    $wshell.SendKeys('^%+') 
    Start-Sleep .3
    $wshell.SendKeys('%a')
}

function toggleVideo {

    $wshell = New-Object -ComObject wscript.shell;
    $wshell.SendKeys('^%+') 
    Start-Sleep .3
    $wshell.SendKeys('%v')
}

while ($true){
    try{
        # Loop to read serial port
        $portName = [System.IO.Ports.SerialPort]::getportnames()

        $port= new-Object System.IO.Ports.SerialPort COM6,9600,None,8,one
        $port.Open()
        Write-Output "Connected to port."
        while ($true) {
            Write-Output "Waiting for input:"
            Write-Output $port.ReadLine()
            Write-Output "Toggling Mute."
            toggleMute
        }
    }
    catch {
      Write-Output "Cannot connect to port. Waiting 1s then trying again."
    }
    finally{
        $port.Close()
    }
    Sleep 1
}

# https://stackoverflow.com/questions/54826083/register-objectevent-from-runspace
# https://stackoverflow.com/questions/31297365/how-to-continuously-read-serial-com-port-in-powershell-and-occasionally-write-to
# https://devblogs.microsoft.com/scripting/use-asynchronous-event-handling-in-powershell/