# Open Terminal with CLI

This guide will show you how to open terminal with CLI when you are scripting in desktop environment.

## Problem

You are doing bash scripting, and you want to open terminal with CLI in the script.

## Solution

### Step 1: Check your terminal emulator

In Ubuntu, the default option is `gnome-terminal`; in Raspbian, the default option is `lxterminal`. Find out the terminal emulator you are using.

### Step 2: Define command to execute after main command

In most cases, you would like the newly opened terminal to stay open after the main command is executed.

1. Keep interact with the terminal after the main command is executed:
    ```bash
    terminate_command="bash"
    ```
2. Keep the terminal open for a certain amount of time:
    ```bash
    terminate_command="sleep 10"
    ```
3. Keep the terminal open forever:
    ```bash
    terminate_command="sleep infinity"
    ```

### Step 3: Open terminal with CLI

```bash title="gnome-terminal"
gnome-terminal -t "Terminal Title" --active -- bash -c "echo \"Hello World\"; $terminate_command"
```

For `gnome-terminal`, you can check the function implementation at [my GitHub](https://github.com/CYCU-AIoT-System-Lab/TPM_Sharing_Scheme/blob/main/common/functions.sh#L234)

```bash title="lxterminal"
lxterminal -t "Terminal Title" -e "echo \"Hello World\"; $terminate_command"
```

For `lxterminal`, you can check the function implementation at [my GitHub](https://github.com/CYCU-AIoT-System-Lab/TPM_Sharing_Scheme/blob/main/common/functions.sh#L252)

## Reference

## Error Correction

If you find any mistakes in the document, please create an [Issue](https://github.com/belongtothenight/belongtothenight.github.io/issues) or a [Pull request](https://github.com/belongtothenight/belongtothenight.github.io/pulls) or leave a message in [Discussions](https://github.com/belongtothenight/belongtothenight.github.io/discussions) or send me a mail directly with the mail icon at the bottom right. Thank you!
