# init
if starting:
    centreX = 0.015
    centreY = 0.03
    sensX = 50
    sensY = 50
    viewSensX = 10
    viewSensY = 10
    system.setThreadTiming(TimingTypes.HighresSystemTimer)
    system.threadExecutionInterval = 20
    x = 0
    y = 0
    rx = 0
    ry = 0
    freelook = True
    viewLatch = True
    moveLatch = True
    joyEnabled = True  # Variável para controlar se o joystick está ativado ou desativado
    lastCommaState = False  # Variável para armazenar o estado anterior da tecla vírgula
    lastDotState = False  # Variável para armazenar o estado anterior da tecla ponto (.)

# Verifica o estado da tecla vírgula para alternar o estado do joystick
currentCommaState = keyboard.getPressed(Key.Comma)  # Estado atual da tecla vírgula

# Se a tecla vírgula foi pressionada e não estava pressionada anteriormente, alterna o estado
if currentCommaState and not lastCommaState:
    joyEnabled = not joyEnabled  # Alterna entre ativado e desativado
    diagnostics.watch(joyEnabled)  # Para depuração: mostra o estado de "joyEnabled"

lastCommaState = currentCommaState  # Atualiza o estado anterior da tecla vírgula

# Verifica o estado da tecla ponto para centralizar o joystick
currentDotState = keyboard.getPressed(Key.Period)  # Estado atual da tecla ponto (.)

# Se a tecla ponto foi pressionada e não estava pressionada anteriormente, centraliza os eixos
if currentDotState and not lastDotState:
    # Centraliza o joystick (zera os eixos)
    rx = 0
    ry = 0
    x = 0
    y = 0
    diagnostics.watch("Joystick Centralizado!")  # Mensagem de depuração

lastDotState = currentDotState  # Atualiza o estado anterior da tecla ponto

# mouse axis - somente atualiza os eixos se o joystick estiver ativado
if joyEnabled:
    if mouse.deltaX:
        if freelook:
            rx += mouse.deltaX * viewSensX
        else:
            moveLatch = True
            x += mouse.deltaX * sensX
            if abs(x) > vJoy[0].axisMax:
                x = vJoy[0].axisMax * x / abs(x)

    if mouse.deltaY:
        if freelook:
            ry += mouse.deltaY * viewSensY
        else:
            moveLatch = True
            y += mouse.deltaY * sensY
            if abs(y) > vJoy[0].axisMax:
                y = vJoy[0].axisMax * y / abs(y)

# recenter - sempre reinicia os valores quando o joystick não estiver em freelook
if not freelook and viewLatch:
    rx = 0
    ry = 0
    viewLatch = False

# freelook control
freelook = mouse.getButton(3) or mouse.middleButton
if mouse.getPressed(3):
    viewLatch = True

# vJoy axis mapping (só atualiza se o joystick estiver ativado)
if joyEnabled:
    vJoy[0].rx = rx
    vJoy[0].ry = ry
    vJoy[0].x = x
    vJoy[0].y = y
else:
    # Se o joystick estiver desativado, mantém os valores atuais, não zera os eixos
    diagnostics.watch("Joystick Desativado, mantendo últimos valores!")
    vJoy[0].rx = vJoy[0].rx  # Mantém o valor atual
    vJoy[0].ry = vJoy[0].ry  # Mantém o valor atual
    vJoy[0].x = vJoy[0].x    # Mantém o valor atual
    vJoy[0].y = vJoy[0].y    # Mantém o valor atual

diagnostics.watch(vJoy[0].x)
diagnostics.watch(vJoy[0].y)
diagnostics.watch(vJoy[0].rx)
diagnostics.watch(vJoy[0].ry)
diagnostics.watch(freelook)
diagnostics.watch(moveLatch)
diagnostics.watch(mouse.getButton(3))
diagnostics.watch(joyEnabled)  # Para depuração: mostra o status de "joyEnabled"
