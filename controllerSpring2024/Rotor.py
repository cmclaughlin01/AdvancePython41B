import opCommand


class Rotor:
    def __init__(self):
        self.lowerAscii = 0x20
        self.upperAscii = 0x80
        self.initShift = 0
        self.position = [0]
        self.counter = 0
        self.executeInt = 0
        self.opCodes = {
            0b000: self.reset,
            0b001: self.increment,
            0b010: self.decrement,
            0b011: self.executeMulti,
            0b100: self.getPosition,
            0b101: self.getPosAtIndex,
            0b110: self.rotorCounter,
            0b111: None
        }

    def reset(self, repeatExe):
        self.counter = 0
        self.position = [0]

    def increment(self, repeatExe):
        nextNumber = self.position[-1] + 1
        self.position.append(nextNumber)
        self.counter += 1
        return self.position[-1]

    def decrement(self, repeatExe):
        nextNumber = self.position[-1] - 1
        self.position.append(nextNumber)
        self.counter += 1
        return self.position[-1]

    def executeMulti(self, repeatExe):
        for i in range(repeatExe):
            nextNumber = self.position[-1] + 1
            self.position.append(nextNumber)
            self.counter += 1
        return self.position[-1]

    def getPosition(self, repeatExe = None):
        return self.position[-1]

    def getPosAtIndex(self, arg):
        return self.position[arg]

    def rotorCounter(self, repeatExe = None):
        return self.counter

    def handleCommand(self, command):
        op = command.op
        self.executeInt = command.argv

        commandCode = self.opCodes.get(op)
        if commandCode:
            # commandCode(self.executeInt)
            return commandCode(self.executeInt)


if __name__ == "__main__":
    rotor = Rotor()
    # cmd_reset = opCommand.Command(0b000)
    # rotor.handleCommand(cmd_reset)

    cmd_increment = opCommand.Command(0b001)
    incremented_char = rotor.handleCommand(cmd_increment)
    print(f"Incremented character: {incremented_char}")

    cmd_exec_n_times = opCommand.Command(0b011, 3)
    exec_n_times_result = rotor.handleCommand(cmd_exec_n_times)
    print(f"Executed 5 increments: {exec_n_times_result}")

    cmd_getPosition = opCommand.Command(0b100)
    current_position = rotor.handleCommand(cmd_getPosition)
    print(f"Current rotor position: {current_position}")

    # # Create and execute a command to get the character at the current position
    cmd_get_character = opCommand.Command(0b101, 2)
    current_character = rotor.handleCommand(cmd_get_character)
    print(f"Character at current position: {current_character}")

    # Create and execute a command to get the rotation counter
    cmd_get_rotorCounter = opCommand.Command(0b110)
    rotorCounter = rotor.handleCommand(cmd_get_rotorCounter)
    print(f"Rotation counter: {rotorCounter}")

    print(rotor.position)
