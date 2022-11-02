"""
CS3B, Assignment #4, Logic gate simulation (Part 1)
Copyright 2021 Zibin Yang
Instructor's solution
"""


class Input:
    """A class representing an input"""

    def __init__(self, owner):
        if not isinstance(owner, LogicGate):
            raise TypeError("Owner should be a type of LogicGate")
        self._owner = owner

    def __str__(self):
        try:
            return str(self.value)
        except AttributeError:
            # It's possible to not have a value at the beginning, so
            # handle the exception properly.
            return "(no value)"

    @property
    def owner(self):
        return self._owner

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        # Normalize the value to bool
        self._value = bool(value)
        # Now that the input value has changed, tell to owner logic gate
        # to re-evaluate
        self.owner.evaluate()


class Output:
    """A class representing an output"""

    def __init__(self):
        self._connections = []

    def __str__(self):
        try:
            return str(self.value)
        except AttributeError:
            # It's possible not to have a value at the beginning
            return "(no value)"

    def connect(self, input_):
        if not isinstance(input_, Input):
            raise TypeError("Output must be connected to an input")
        # If the input is not already in the list, add it; alternative is to
        # use a set.
        if input_ not in self.connections:
            self.connections.append(input_)
        try:
            # Set the input's value to this output's value upon connection
            input_.value = self._value
        except AttributeError:
            # If self.value is not there, skip it
            pass

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        # Normalize the value to bool
        self._value = bool(value)
        # After the output value changes, set all the connected inputs
        # to the same value.
        for connection in self.connections:
            connection.value = self.value

    @property
    def connections(self):
        return self._connections


class CostMixin:
    """ A class expands logic gates capacity like querying the cost """

    COST_MULTIPILER = 10
    
    def __init__(self, number_of_components):
        self._number_of_components = number_of_components
        self._cost = 0

    @property
    def number_of_components(self):
        return self._number_of_components

    @property
    def cost(self):
        self._cost = COST_MULTIPILER * (self._number_of_components ** 2)


class LogicGate:
    """Base class for all logic gates."""

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


class UnaryGate(LogicGate):
    """A class representing logic gate with a single input."""

    def __init__(self, name):
        super().__init__(name)
        self._input = Input(self)
        self._output = Output()

    def __str__(self):
        return (f"LogicGate {self.name}: input={self.input}, "
                f"output={self.output}")

    @property
    def input(self):
        return self._input

    @property
    def output(self):
        return self._output


class BinaryGate(LogicGate):
    """A class representing logic gate with two inputs."""

    def __init__(self, name):
        super().__init__(name)
        self._input0 = Input(self)
        self._input1 = Input(self)
        self._output = Output()

    def __str__(self):
        return (f"LogicGate {self.name}: input0={self.input0}, "
                f"input1={self.input1}, output={self.output}")

    @property
    def input0(self):
        return self._input0

    @property
    def input1(self):
        return self._input1

    @property
    def output(self):
        return self._output


class NotGate(UnaryGate):
    def evaluate(self):
        try:
            self.output.value = not self.input.value
        except AttributeError:
            pass


class AndGate(BinaryGate):
    def evaluate(self):
        try:
            # This may throw an exception, if one of the input is not yet set,
            # which is possible in the normal course of evaluation, because
            # setting the first input will kick off the evaluation.  So just
            # don't set the output.
            self.output.value = self.input0.value and self.input1.value
        except AttributeError:
            pass


class OrGate(BinaryGate):
    def evaluate(self):
        try:
            self.output.value = self.input0.value or self.input1.value
        except AttributeError:
            pass


class XorGate(BinaryGate):
    def evaluate(self):
        try:
            # Assume the value is bool, != is same as xor
            self.output.value = (self.input0.value != self.input1.value)
        except AttributeError:
            pass


def test():
    """Umbrella test function"""
    tests = [
        test_input,
        test_output,
        test_not,
        test_and,
        test_or,
        test_xor,
        test_not_not,
        test_and_not,
    ]
    for t in tests:
        print("Running " + t.__name__ + " " + "-" * 20)
        t()


def test_input():
    input_ = Input(NotGate("test"))
    print("Initially, input_ is:", input_)
    try:
        print(input_.value)
        print("Failed: input_.value exists before it's set, which should not happen!")
    except AttributeError:
        print("Succeeded: input_.value doesn't exist before it's set.")
    input_.value = True
    print("After set to True, input_ is:", input_)


def test_output():
    output = Output()
    print("Initially, output is:", output)
    try:
        print(output.value)
        print("Failed: output.value exists before it's set, which should not happen!")
    except AttributeError:
        print("Succeeded: output.value doesn't exist before it's set.")
    output.value = True
    print("After set to True, output is:", output)

def test_not():
    not_gate = NotGate("not")
    not_gate.input.value = True
    print(not_gate)
    not_gate.input.value = False
    print(not_gate)


def test_and():
    and_gate = AndGate("and")
    print("AND gate initial state:", and_gate)
    and_gate.input0.value = True
    print("AND gate with 1 input set", and_gate)
    and_gate.input1.value = False
    print("AND gate with 2 inputs set:", and_gate)
    and_gate.input1.value = True
    print("AND gate with 2 inputs set:", and_gate)


def test_or():
    or_gate = OrGate("or")
    or_gate.input0.value = False
    or_gate.input1.value = False
    print(or_gate)
    or_gate.input1.value = True
    print(or_gate)


def test_xor():
    xor_gate = XorGate("xor")
    xor_gate.input0.value = False
    xor_gate.input1.value = False
    print(xor_gate)
    xor_gate.input1.value = True
    print(xor_gate)


def test_not_not():
    not_gate1 = NotGate("not1")
    not_gate2 = NotGate("not2")
    not_gate1.output.connect(not_gate2.input)
    print(not_gate1)
    print(not_gate2)
    print("Setting not-gate input to False...")
    not_gate1.input.value = False
    print(not_gate1)
    print(not_gate2)


def test_and_not():
    and_gate = AndGate("and")
    not_gate = NotGate("not")
    and_gate.output.connect(not_gate.input)
    and_gate.input0.value = True
    and_gate.input1.value = False
    print(and_gate)
    print(not_gate)
    and_gate.input1.value = True
    print(and_gate)
    print(not_gate)


if __name__ == '__main__':
    test()