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


function GetInput {
    param ($input)

}

while ($true) {
    try {
        # $portName = [System.IO.Ports.SerialPort]::getportnames()
        # Open Port Object
        $port = new-Object System.IO.Ports.SerialPort COM4, 9600, None, 8, one
        $port.Open()
        Write-Output "Connected to port."
        # Start background job to check for button presses
        $readJob = Start-Job -ScriptBlock {     
            while ($true) {
                # $input.ReadLine()
                $wshell = New-Object -ComObject wscript.shell;
                $wshell.SendKeys($port.ReadLine()) 
                # Start-Sleep .3
                # $wshell.SendKeys('%a')
                
        } } -ArgumentList $port
        while($true){
            Write-Output Get-Job $readJob
        }
    }
    catch {
        Write-Output "Cannot connect to port. Waiting 1s then trying again."
        Start-Sleep 1
    }
    finally {
        # Stop-Job -Id $readJob
        $port.Close()
    }
}

# https://stackoverflow.com/questions/54826083/register-objectevent-from-runspace
# https://stackoverflow.com/questions/31297365/how-to-continuously-read-serial-com-port-in-powershell-and-occasionally-write-to
# https://devblogs.microsoft.com/scripting/use-asynchronous-event-handling-in-powershell/