"""
CS3B, Assignment #5, Logic gate simulation (Part 2)
Yingshi Liu
"""


# Classes that have "has-a" relationship with logic gates(AndGate, OrGate...)
# E.g. AndGate has Input, Output and CostMixin


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
        # connect can trigger value change both direction
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

    COST_MULTIPLIER = 10
    
    def __init__(self, number_of_components):
        self._number_of_components = number_of_components
        self._cost = 0

    @property
    def number_of_components(self):
        return self._number_of_components

    @property
    def cost(self):
        self._cost = CostMixin.COST_MULTIPLIER * (self._number_of_components ** 2)
        return self._cost

# Classes that have "is-a" relationship with logic gates(AndGate, OrGate...)
# E.g. AndGate is a LogicGate(), is a NodeMixin()

class NodeMixin:
    """ A class that can link multiple logic gates together in the Circuit class """
    """ Similar with the dataStack class in the lecture """

    def __init__(self):
        self._next = None

    @property
    def next(self):
        if self._next:
            return self._next
        return None

    @next.setter
    def next(self, node):
        if not isinstance(node, LogicGate):
            raise TypeError(f"The input node {node} is not a LogicGate instance.")
        self._next = node

    def __str__(self):
        return "Node id={}, next={}".format(
            hex(id(self)), "(none)" if self.next is None else hex(id(self.next)))


class LogicGate:
    """Base class for all logic gates."""

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


class UnaryGate(LogicGate, NodeMixin):
    """A class representing logic gate with a single input."""

    def __init__(self, name, circuit=None):
        super().__init__(name)
        NodeMixin.__init__(self)
        self._input = Input(self)
        self._output = Output()
        self._cost = CostMixin(2).cost
        # test circuit is the right type
        if not isinstance(circuit, Circuit):
            raise TypeError(f"input circuit is not the right type")
        circuit.add(self)

    def __str__(self):
        return (f"LogicGate {self.name}: input={self.input}, "
                f"output={self.output}")

    @property
    def input(self):
        return self._input

    @property
    def output(self):
        return self._output

    @property
    def cost(self):
        return self._cost


class BinaryGate(LogicGate, NodeMixin):
    """A class representing logic gate with two inputs."""

    def __init__(self, name,  circuit=None):
        super().__init__(name)
        NodeMixin.__init__(self)
        self._input0 = Input(self)
        self._input1 = Input(self)
        self._output = Output()
        self._cost = CostMixin(3).cost
        # test circuit is the right type
        if not isinstance(circuit, Circuit):
            raise TypeError(f"input circuit is not the right type")
        circuit.add(self)

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

    @property
    def cost(self):
        return self._cost

# Classes that are a specific gate


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

# Class that keeps track of all logic gates belonging to a specific  circuit.

class Circuit:
    """ A class that keeps track of all logic gates belonging to a specific circuit """

    def __init__(self):
        self._cost = 0
        # self._top = None

    @property
    def cost(self):
        start = self._top
        while start is not None:
            self._cost += start.cost
            start = start.next
        return self._cost

    def add(self, gate):
        try:
            if not isinstance(gate, NodeMixin):
                raise TypeError(f"The input node is not the right type of NodeMixin")
            gate.next = self._top
            self._top = gate
        except AttributeError:
            self._top = gate


    def __str__(self):
        start = self._top
        returned_str = ""
        while start is not None:
            returned_str += "(" + str(start) + ")"
            start = start.next
        return returned_str


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
    circuit = Circuit()
    input_ = Input(NotGate("test", circuit))
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
    circuit = Circuit()
    not_gate = NotGate("not", circuit)
    not_gate.input.value = True
    print(not_gate)
    not_gate.input.value = False
    print(not_gate)
    print(circuit)
    print(circuit.cost)


def test_and():
    circuit = Circuit()
    and_gate = AndGate("and", circuit)
    print("AND gate initial state:", and_gate)
    and_gate.input0.value = True
    print("AND gate with 1 input set", and_gate)
    and_gate.input1.value = False
    print("AND gate with 2 inputs set:", and_gate)
    and_gate.input1.value = True
    print("AND gate with 2 inputs set:", and_gate)
    print(circuit)
    print(circuit.cost)


def test_or():
    circuit = Circuit()
    or_gate = OrGate("or", circuit)
    or_gate.input0.value = False
    or_gate.input1.value = False
    print(or_gate)
    or_gate.input1.value = True
    print(or_gate)


def test_xor():
    circuit = Circuit()
    xor_gate = XorGate("xor", circuit)
    xor_gate.input0.value = False
    xor_gate.input1.value = False
    print(xor_gate)
    xor_gate.input1.value = True
    print(xor_gate)


def test_not_not():
    circuit = Circuit()
    not_gate1 = NotGate("not1", circuit)
    not_gate2 = NotGate("not2", circuit)
    print(f"After connection")
    not_gate1.output.connect(not_gate2.input)
    print(not_gate1)
    print(not_gate2)
    print("Setting not-not_gate1 input to False...")
    not_gate1.input.value = False
    print(not_gate1)
    print(not_gate2)
    print(f"Cost of not_gate1 is {not_gate1.cost}")
    print(f"Cost of NOT-NOT circuit is {circuit.cost}")


def test_and_not():
    circuit = Circuit()
    and_gate = AndGate("and", circuit)
    not_gate = NotGate("not", circuit)
    print(f"After connection")
    and_gate.output.connect(not_gate.input)
    print("Setting and_gate input0 to True and input1 to False")
    and_gate.input0.value = True
    and_gate.input1.value = False
    print(and_gate)
    print(not_gate)
    print("Setting and_gate input1 to True")
    and_gate.input1.value = True
    print(and_gate)
    print(not_gate)
    print(f"Cost of and_gate is {and_gate.cost}")
    print(f"Cost of not_gate is {not_gate.cost}")
    print(f"Cost of NOT-NOT circuit is {circuit.cost}")


def full_adder(a, b, ci):
    """ Function that builds the 1-bit full adder circuit """

    # Get Sum
    circuit = Circuit()
    xor_gate1 = XorGate("Xor Gate", circuit)
    xor_gate2 = XorGate("Xor Gate", circuit)
    xor_gate2.output.connect(xor_gate1.input0)
    xor_gate2.input0.value = a
    xor_gate2.input1.value = b
    xor_gate1.input1.value = ci
    # print(f"gate1: {xor_gate1}")
    # print(f"gate2: {xor_gate2}")
    sum = xor_gate1.output.value

    # Get Co
    # 1st AndGate: ((a XOR b) and ci)
    andgate1 = AndGate("and1", circuit)
    andgate1.input0.value = xor_gate2.output.value
    andgate1.input1.value = ci
    print(f"((a XOR b) and ci): {andgate1}")

    # 2nd AndGate: a AND b
    andgate2 = AndGate("and2", circuit)
    andgate2.input0.value = a
    andgate2.input1.value = b
    print(f"a AND b: {andgate2}")

    # OrGate
    orgate = OrGate("or", circuit)
    andgate1.output.connect(orgate.input0)
    andgate2.output.connect(orgate.input1)
    co = orgate.output.value
    print(f"orgate: {orgate}")
    print(f"co: {co}")
    print(f"sum co: {sum} {co}")

    return (sum, co, circuit.cost)


if __name__ == '__main__':
    # test()
    result = full_adder(True, False, True)
    print(result)
    # test_and_not()
