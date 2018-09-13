import unittest
import StringIO

from ztag.stream import Updater, UpdateRow


class UpdaterTestCase(unittest.TestCase):
    FREQUENCY = 1.0

    def setUp(self):
        pass

    def test_updater(self):
        """
        Check that the updater runs as expected.
        """
        output = StringIO.StringIO()
        updater = Updater(output=output, frequency=self.FREQUENCY)
        skipped = 0
        handled = 0
        expected = [UpdateRow.get_csv_labels()]
        for i in range(0, 100000):
            skipped += 1
            handled += 2
            row = UpdateRow(
                skipped=skipped,
                handled=handled,
                updated_at=float(i) / 100.0,
                prev=updater.prev)

            if not updater.prev or (row.time - updater.prev.time) >= updater.frequency:
                expected.append(row.get_csv())

            updater.put_update(row)

        self.assertEquals("\n".join(expected) + "\n", output.getvalue())
        updater.close()
