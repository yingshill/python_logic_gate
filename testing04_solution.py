"""
Yingshi Liu
Testing file
CS3B, Assignment #4, Logic gate simulation (Part 1)
"""
import operator
import unittest
import unittest.mock
from assignment04 import *


class MockGate(LogicGate):
    """
    A gate used for mock testing.  This is more advanced form of testing and
    is not a required topic.
    """

    def __init__(self, name):
        self.evaluate_called = False

    def evaluate(self):
        # In this mock version it doesn't set the output, but just remember
        # that it's been called.
        self.evaluate_called = True


class MockInput(Input):
    """
    Input used for testing
    """

    def __init__(self):
        pass

    # Override Input.value for testing
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        # In this mock version it doesn't ask the owner to evaluate, reducing
        # dependencies.
        self._value = value


class InputTest(unittest.TestCase):
    def setUp(self):
        self.mock_gate = MockGate("mock")
        self.input = Input(self.mock_gate)

    def testInit(self):
        self.assertIs(self.mock_gate, self.input.owner)
        self.assertTrue(not hasattr(self.input, "value") or self.input.value is None)
        self.assertTrue(not hasattr(self.input, "_value") or self.input._value is None)

    def testInitFailure(self):
        with self.assertRaises(TypeError):
            input0 = Input("bad owner")

    def testStr(self):
        # Make sure __str__ can handle no value being set
        self.assertEqual(str, type(self.input.__str__()))
        self.assertEqual("(no value)", self.input.__str__())

    def testValueGetterSetterTrue(self):
        self.input.value = True
        self.assertTrue(self.input.value)
        self.assertTrue("True", self.input.__str__())

    def testValueGetterSetterFalse(self):
        self.input.value = False
        self.assertFalse(self.input.value)
        self.assertTrue("False", self.input.__str__())

    def testValueSetterNormalizeToBool(self):
        self.input.value = 1
        self.assertIs(True, self.input.value)

        self.input.value = ""
        self.assertIs(False, self.input.value)

    def testValueSetterCallOwnerEvaluate(self):
        self.input.value = True
        self.assertTrue(self.input.owner.evaluate_called,
                        "Setting input value didn't call owner's evaluate (is it called in output's getter?)")

    def testCallEvaluateUsingMock(self):
        # Use spec= to pass isinstance() teset in Input.__init__().
        # https://stackoverflow.com/questions/11146725/isinstance-and-mocking
        # https://docs.python.org/3/library/unittest.mock.html#the-mock-class
        mock_logic_gate = unittest.mock.MagicMock(spec=LogicGate)
        # Hmm, have to manually crate the evaluate() method, otherwise it
        # doesn't exist!
        mock_logic_gate.evaluate = unittest.mock.MagicMock(name="evaluate")
        input_ = Input(mock_logic_gate)
        self.assertIs(mock_logic_gate, input_.owner)
        input_.value = True
        mock_logic_gate.evaluate.assert_called_once()

    # An unsuccessful test using mock to see if evaluate() is called
    @unittest.skip("This test doesn't entirely work")
    @unittest.mock.patch("assignment04_instructor_solution.LogicGate")
    def testMock1(self, mock_logic_gate_constructor):
        mock_gate = mock_logic_gate_constructor.return_value
        # mock_gate unfortunately is no longer instance of LogicGate, so this
        # triggers the type-check in Input.__init__().  Remove that, and the
        # rest does work.
        input_ = Input(mock_gate)
        self.assertIs(mock_gate, input_.owner)
        input_.value = True
        mock_gate.evaluate.assert_called_once()


class OutputTest(unittest.TestCase):
    def setUp(self):
        self.output = Output()

    def testInit(self):
        self.assertTrue(not hasattr(self.output, "value") or self.output.value is None)
        self.assertTrue(not hasattr(self.output, "_value") or self.output._value is None)

    def testStr(self):
        # Make sure __str__ can handle no value being set
        self.assertEqual(str, type(self.output.__str__()))
        self.assertEqual("(no value)", self.output.__str__())

    def testValueGetterSetterTrue(self):
        self.output.value = True
        self.assertTrue(self.output.value)
        self.assertTrue("True", self.output.__str__())

    def testValueGetterSetterFalse(self):
        self.output.value = False
        self.assertFalse(self.output.value)
        self.assertTrue("False", self.output.__str__())

    def testConnect(self):
        input0 = MockInput()
        input1 = MockInput()

        self.output.connect(input0)
        self.assertIn(input0, self.output.connections,
                      "Output should put input0 in its connections")

        self.output.connect(input1)
        self.assertIn(input0, self.output.connections,
                      "Output should still have input0 in its connections")
        self.assertIn(input1, self.output.connections,
                      "Output should put input1 in its connections")

    def testConnectFailure1(self):
        with self.assertRaises(TypeError):
            self.output.connections("bad input")

    def testConnectFailure2(self):
        input0 = MockInput()
        self.output.connect(input0)
        self.output.connect(input0)
        # Do a manual count that handles connections being either list or set.
        self.assertEqual(1, len([input_ for input_ in self.output.connections
                                 if input_ is input0]))

    def testConnectedValueSetterSetInputValue1(self):
        # Test the sequence: set-value, connect
        input0 = MockInput()
        input1 = MockInput()

        for value in [False, True]:
            with self.subTest(str(value)):
                self.output.value = value
                self.output.connect(input0)
                self.output.connect(input1)
                self.assertEqual(value, input0.value)
                self.assertEqual(value, input1.value)

    def testConnectedValueSetterSetInputValue2(self):
        for value in [False, True]:
            with self.subTest(str(value)):
                # Test the sequence: connect, set-value
                input0 = MockInput()
                input1 = MockInput()

                # If the implementation doesn't handle when output.value isn't
                # set, this might raise an exception.
                self.output.connect(input0)
                self.output.connect(input1)

                self.output.value = value

                self.assertEqual(value, input0.value)
                self.assertEqual(value, input1.value)


class LogicGateTest(unittest.TestCase):
    def setUp(self):
        self.binary_gate_types_map = {
            AndGate: operator.and_,
            OrGate: operator.or_,
            XorGate: operator.xor,
        }

        self.binary_gate_types = self.binary_gate_types_map.keys()

        self.gate_types = list(self.binary_gate_types) + [NotGate]

        self.input_values = [True, False]

    def testName(self):
        name = "name"
        for gate_type in self.gate_types:
            with self.subTest(f"{gate_type.__name__=}"):
                gate = gate_type(name)
                self.assertEqual(name, gate.name)

    def testSetNameInputOutput(self):
        for gate_type in self.gate_types:
            with self.subTest(f"{gate_type.__name__=}"):
                gate = gate_type(gate_type.__name__)

                with self.assertRaises(AttributeError):
                    gate.name = "not possible"

                with self.assertRaises(AttributeError):
                    if gate_type in self.binary_gate_types:
                        gate.input0 = "not possible"
                    else:
                        gate.input = "not possible"

                with self.assertRaises(AttributeError):
                    gate.output = "not possible"

    def testStr(self):
        for gate_type in self.gate_types:
            with self.subTest(f"{gate_type.__name__=}"):
                self.assertEqual(str, type(gate_type(gate_type.__name__).__str__()),
                                 "{}.__str__() didn't return str".format(gate_type.__name__))

    def testNotGate(self):
        not_gate = NotGate("not")
        for i in self.input_values:
            with self.subTest(f"input={i}"):
                not_gate.input.value = i
                self.assertEqual(not i, not_gate.output.value)

    def testNotGateOutputNotSet(self):
        # If implementation chooses to set value upon initialization, it should be None
        not_gate = NotGate("not")
        if hasattr(not_gate.output, "value"):
            self.assertIsNone(not_gate.output.value)

    def testBinaryGateOutputNotSet(self):
        # If implementation chooses to set value upon initialization, it should be None
        for gate_type in self.binary_gate_types:
            with self.subTest(f"Testing {gate_type.__name__}"):
                gate = gate_type(gate_type.__name__)
                if hasattr(gate.output, "value"):
                    self.assertIsNone(gate.output.value)

                    gate.input0.value = True
                    self.assertIsNone(gate.output.value,
                                      "Did evaluate() forget to check if input values are not set?")

    def testBinaryGate(self):
        for gate_type, op in self.binary_gate_types_map.items():
            gate = gate_type(gate_type.__name__)
            for a in self.input_values:
                for b in self.input_values:
                    with self.subTest(f"Testing {gate_type.__name__}, {a}, {b}"):
                        gate.input0.value = a
                        gate.input1.value = b
                        self.assertEqual(op(a, b), gate.output.value,
                                         f"{a} {gate_type.__name__} {b} = {gate.output.value}")

    def testConnectedNotNot(self):
        not_gate1 = NotGate("not1")
        not_gate2 = NotGate("not2")
        not_gate1.output.connect(not_gate2.input)

        for i in self.input_values:
            with self.subTest(i):
                not_gate1.input.value = i
                self.assertEqual(i, not_gate2.output.value)

    def testConnectedAndNot(self):
        and_gate = AndGate("and")
        not_gate = NotGate("not")
        and_gate.output.connect(not_gate.input)

        for a in self.input_values:
            for b in self.input_values:
                with self.subTest(f"{a=}, {b=}"):
                    and_gate.input0.value = a
                    and_gate.input1.value = b
                    self.assertEqual(not (a and b), not_gate.output.value)


if __name__ == "__main__":
    unittest.main()