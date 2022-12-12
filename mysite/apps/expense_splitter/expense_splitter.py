import pandas


class Event:

    def __init__(self, description, members=None):
        self.description = description
        self._members = []
        self.expenses = []

        self.add_member(members)

    def save(self):
        event = dict(
            description=self.description,
            members=self.members,
            expenses=self.expenses
        )

    def load(self, event_dict):
        self.description = event_dict.get("description")
        self._members = event_dict.get("members")
        self.expenses = event_dict.get("expenses")

    @property
    def expense_grid(self):
        grid = pandas.DataFrame([t["split"] for t in self.expenses], columns=self.members).fillna(0.)
        return grid

    @property
    def summary(self):
        final = self.expense_grid.sum()

        creditors = final.loc[final <= 0].sort_values(ascending=True).copy()
        debtors = final.loc[final > 0].sort_values(ascending=False).copy()

        summary = dict((m, {"amount": final.loc[m]}) for m in self.members)
        for i, (m, v) in enumerate(zip(debtors.index, debtors.values)):
            owe = v
            for c_m, c_v in zip(creditors.index, creditors.values):
                if owe + c_v <= 0.:
                    summary[m][c_m] = owe
                    summary[c_m][m] = - owe
                    creditors.loc[c_m] = owe + c_v
                    break
                else:
                    summary[m][c_m] = - c_v
                    summary[c_m][m] = c_v
                    creditors.loc[c_m] = 0
                    owe += c_v

        return summary

    def add_member(self, names):
        if isinstance(names, str):
            names = [names]
        self._members = sorted(set(self.members + names))

    @property
    def members(self):
        return self._members

    def add_expense(self, description, paying_member, paid_amount, members_to_split=None, split_amount=None):
        assert paying_member in self.members, "Invalid transaction, paying member not found"
        assert True if members_to_split is None else all(m in self.members for m in members_to_split), \
            "Invalid transaction, splitting member not found"
        assert sum(split_amount) <= paid_amount if split_amount else True, "Split amount total is more than paid"

        num_members = len(self.members)
        split_by_members = dict((m, 0.) for m in self.members)
        # if no split defined, split equal
        if not members_to_split:
            split_by_members = dict((m, paid_amount / num_members) for m in self.members)
        # if split members defined but not split amount, split equally between split members
        elif not split_amount:
            split_by_members.update(
                dict((m, paid_amount / len(members_to_split)) for m in members_to_split)
            )
        # if both split members and split amount defined, record as specified
        else:
            split_by_members.update(
                dict((m, amt) for m, amt in zip(members_to_split, split_amount))
            )
            if sum(split_amount) < paid_amount:
                split_by_members[paying_member] += paid_amount - sum(split_amount)
        split_by_members[paying_member] -= paid_amount

        expense_info = dict(
            description=description,
            split=split_by_members,
            paid={paying_member: paid_amount}
        )
        self.expenses.append(expense_info)
        return expense_info


if __name__ == '__main__':
    test = Event("test", "c")
    test.add_member(["a", "b"])

    test.add_expense("t1", "a", 100)
    test.add_expense("t1", "a", 100, ["c"])
    test.add_member(["c", "d"])
    test.add_expense("t1", "c", 100)
    test.add_expense("t1", "d", 100, ["a", "b", "c"])
    test.add_expense("t1", "a", 100, ["a", "b"], [50, 50])
    test.add_expense("t1", "b", 100, ["a", "b", "c"], [10, 20, 10])

    test.summary

    pass
