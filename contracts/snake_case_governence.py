    @export
    def set_governence_token(address: str):
        assert ctx.owner == ctx.caller
        assert disable_governence_contract_change.get() == 0
        governence_contract.set(address)
    
    @export
    def disable_contract_changes():
        assert ctx.owner == ctx.caller
        disable_governence_contract_change.set(1)
    
    @export
    def forward_transaction_fee_rewards():
        assert disable_changing_contract.get() == 1
        amount = currency.balance_of(ctx.this)
        currency.transfer(amount, governence_contract.get())
