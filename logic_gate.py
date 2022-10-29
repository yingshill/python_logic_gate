"""
Yingshi Liu
Assignment04
Oct 28, 2022
"""

class Input:

    def __init__(self, owner):
        """ Handle owner typeerror, here LogicGate() need to be implemented"""
        if isinstance(owner, LogicGate):
            self.owner = owner
        else:
            raise TypeError("Input doesn't have a right logic gate.")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        """ Need to evaluate whether it is a boolean"""
        self._value = bool(new_value)
        self.owner.evaluate()

    def __str__(self):
        """ Handle value, need to use owner's property to test"""
        try:
            return f"(\"{self._value}\")"
        except AttributeError as e:
            print(f"1st error message from try except block: {e}")
            return f"(\"no value\")"


class Output:

    def __init__(self):
        pass

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        """ Need to evaluate whether it is a boolean"""
        self._value = bool(new_value)

    def __str__(self):
        """ Handle value, need to use owner's property to test"""
        try:
            return f"(\"{self._value}\")"
        except AttributeError as e:
            print(f"Output class's value hasn't been set up properly: {e}")
        return f"(\"no value\")"


class LogicGate:

    def __init__(self, name):
        self._name = name
        self._input0 = Input(self)
        self._input1 = Input(self)
        self._output = Output()

    @property
    def name(self):
        return self._name

    @property
    def input0(self):
        return self._input0

    @property
    def input1(self):
        return self._input1

    @property
    def output(self):
        return self._output

    def __str__(self):
        try:
            return f"Gate {self.name}: input0={self.input0.value}, input1={self.input1.value}, output={self.output.value}"
        except AttributeError as e:
            return f"Only one input is set up"

    def evaluate(self):
        try:
            result = self.input0.value and self.input1.value
            print(f"result in evaluate(): {result}")
            self.output.value = result
        except AttributeError as e:
            print(f"Logic Gate error: only one input value is set")
            self._output._value = "not set"


class AndGate(LogicGate):

    def __init__(self, name):
        super().__init__(name)

    def evaluate(self):
        try:
            result = self.input0.value and self.input1.value
            self.output.value = result
        except AttributeError as e:
            print(f"And Gate error: only one input value is set")
            self._output._value = "not set"


class OrGate(LogicGate):

    def __init__(self, name):
        super().__init__(name)

    def evaluate(self):
        try:
            result = self.input0.value or self.input1.value
            self.output.value = result
        except AttributeError as e:
            self._output._value = "not set"


class XorGate(LogicGate):

    def __init__(self, name):
        super().__init__(name)

    def evaluate(self):
        try:
            if self.input0.value and self.input1.value:
                result = False
            else:
                result = self.input0.value or self.input1.value
            self.output.value = result
        except AttributeError as e:
            print(f"only one input value is set")
            self._output._value = "not set"


class NotGate(LogicGate):

    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        try:
            return f"Gate {self.name}: input0={self.input0.value}, output={self.output.value}"
        except AttributeError as e:
            return f"NotGate __str__: input value is not set yet"

    def evaluate(self):
        try:
            self.input0.value
            result = not self.input0.value
            self.output.value = result
        except AttributeError as e:
            print(f"Not gate evaluate: input value is not set")
            self._output._value = "not set"


def test_input():
    not_gate = NotGate("test")
    input0 = not_gate.input0
    print("Initially, input_ is:", input0)
    try:
        print(input.value)
        print("Failed: input_.value exists before it's set, which should not happen!")
    except AttributeError:
        print("Succeeded: input_.value doesn't exist before it's set.")
    input0.value = True
    print("After set to True, input_ is:", input)


def test_output():
    not_gate = NotGate("test")
    output = not_gate.output
    print("Initially, output is:", output)
    try:
        print(output.value)
        print("Failed: output.value exists before it's set, which should not happen!")
    except AttributeError:
        print("Succeeded: output.value doesn't exist before it's set.")
    output.value = True
    print("After set to True, output is:", output)


def test_AndGate():
    and_gate = AndGate("not")
    print(f"Initially, and_gate is: {and_gate}")
    and_gate.input0.value = True
    and_gate.input1.value = False
    print(f"{and_gate}")
    and_gate.input0.value = False
    print(f"{and_gate}")
    and_gate.input0.value = True
    and_gate.input1.value = True
    print(f"{and_gate}")


def test_NotGate():
    not_gate = NotGate("not")
    print(f"Initially, not_gate is: {not_gate}")
    not_gate.input0.value = True
    print(f"output value has been set to be with input0 {not_gate.input0.value}: {not_gate.output.value}")
    print(f"note_gate after value set: {not_gate}")
    not_gate.input0.value = False
    print(f"output value has been set to be with input0 {not_gate.input0.value}: {not_gate.output.value}")
    print(f"Not_gate after value set: {not_gate}")


def test_OrGate():

    or_gate = OrGate("or")
    print(f"Initially, or_gate is: {or_gate}")
    or_gate.input0.value = True
    or_gate.input1.value = False
    print(f"{or_gate}")
    or_gate.input0.value = False
    print(f"{or_gate}")
    or_gate.input0.value = True
    or_gate.input1.value = True
    print(f"{or_gate}")

def test_XorGate():

    xor_gate = XorGate("xor")
    print(f"Initially, or_gate is: {xor_gate}")
    xor_gate.input0.value = True
    xor_gate.input1.value = False
    print(f"{xor_gate}")
    xor_gate.input0.value = False
    print(f"{xor_gate}")
    xor_gate.input0.value = True
    xor_gate.input1.value = True
    print(f"{xor_gate}")

if __name__ == "__main__":
    test_input()
    test_output()
    test_NotGate()
    test_AndGate()
    test_OrGate()
    test_XorGate()