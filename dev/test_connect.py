from PyQt6.QtCore import QObject, pyqtSignal


class Foo(QObject):

    # Define a new signal called 'trigger' that has no arguments.
    trigger = pyqtSignal()

    def connect_and_emit_trigger(self):
        # Connect the trigger signal to a slot.
        self.trigger.connect(self.handle_trigger)

        # Emit the signal.
        self.trigger.emit()

    def handle_trigger(self):
        # Show that the slot has been called.
        print("trigger signal received")

if __name__ == "__main__":
    print(1)
    foo = Foo()
    print(2)
    foo.trigger.emit()
    print(3)
    Foo.trigger.emit()
    print(4)