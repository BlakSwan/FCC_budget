class Category(object):
    def __init__(self, category):
        self.__class__.__name__ = category.lower()
        self.name = category
        self.ledger = []
           
    def __repr__(self):
        return self.get_print()
            
    def get_print(self):
        item_list = []
        item_list.append(self.name.center(30,"*")+'\n')
        for item in self.ledger:
            desc = '{:23.23}'.format(item['description'])
            amount = '{:>7}'.format('%.2f' % item['amount'])
            line = desc + amount +'\n'
            item_list.append(line)
        total = self.get_balance()
        line = 'Total: ' + str(total)
        item_list.append(line)
        return(''.join(item_list))

        
    def deposit(self, amount, description=''):
        depo_dict = {"amount": amount, "description": description}
        self.ledger.append(depo_dict)
        
    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            with_dict = {"amount": amount * -1, "description": description}
            self.ledger.append(with_dict)
            return True
        else:
            return False
        
    def get_balance(self):
        balance = 0
        for dict in self.ledger:
            balance += dict['amount']
        return balance
        
    def transfer(self, amount, recipient):
        if self.check_funds(amount):
            self.withdraw(amount, description = f'Transfer to {recipient.name}')
            recipient.deposit(amount, f'Transfer from {self.name}')
            return True
        else:
            return False
        
    def check_funds(self, amount):
        if amount > self.get_balance():
            return False
        else:
            return True

def create_spend_chart(categories):
    item_list = []
    total_spent = {'total_spent': [], categories[0].name: [], categories[1].name: [], categories[2].name: []}
    item_list.append('Percentage spent by category\n')
    
    for i, x in enumerate(categories):
        for lx in x.ledger:
            if lx['amount'] < 0:
                total_spent['total_spent'].append(lx['amount'])
                total_spent[x.name].append(lx['amount'])
    sum_total_spent = 0
    sum_total_cat = {}
    for i, x in enumerate(total_spent):
        if x == 'total_spent':
            sum_total_spent = sum(total_spent[x])
        else:
            sum_total_cat[x] = sum(total_spent[x])
    for row in range(100, -10, -10):              
        row_list = []
        row_list.append(str('{:3d}'.format(row))+ '|')
        for i, x in enumerate(sum_total_cat):
            if (sum_total_cat[x]/sum_total_spent*100) > row:
                row_list.append(' o ')
            else:
                row_list.append('   ')
        row_list.append(' \n')
        line = ''.join(row_list)   
        item_list.append(line)
    item_list.append('    ----------\n')
    longest = max([len(categories[i].name) for i, x in enumerate(categories)])
    for row in range(longest):
        row_list = []
        row_list.append('    ')
        for i, lx in enumerate(categories):
            try:
                row_list.append(' ' + categories[i].name[row] + ' ')
            except IndexError:
                row_list.append('   ')
        if row < longest-1:
            row_list.append(' \n')
        else:
            row_list.append(' ')
        line = ''.join(row_list)
        item_list.append(line)
    return(''.join(item_list))
