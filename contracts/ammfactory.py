import submission
import currency
allExchanges = Variable()
disableChangingContract = Variable()
governenceContract = Variable()
@construct
def seed():
    ctx.owner = ctx.caller
    governenceContract.set(ctx.this)
@export
def createChildContract(AMMAddress: str, tokenAddress: str):
    contract = """# you must transfer 0.01 TAU and the equivalent in your Token to ctx.this to start liquidity. It's a hack, but I really don't want to think about liquidity logic any more
# your currency must have the following and follow the currency format: approve, transfer_from, balance_of, transfer
import currency
import basetoken
liquidityTokenBalance = Hash(default_value=0)
totalLiquidityTokens = Hash(default_value=100)
@export 
def tradeTAUForToken(amount: int, fromAddress: str):
    assert amount > 0, 'Cannot send negative balance'
    inputReserve = currency.balance_of(ctx.this)
    outputReserve = basetoken.balance_of(ctx.this)
    currency.transfer_from(amount, ctx.this, fromAddress)
    assert inputReserve > 0 and outputReserve > 0
    numerator = amount * outputReserve
    denominator = (inputReserve) + amount
    amount = (numerator / denominator)
    basetoken.transfer(amount, fromAddress)
@export
def tradeTokenForTAU(amount: int, fromAddress: str):
    assert amount > 0, 'Cannot send negative balance'
    outputReserve = currency.balance_of(ctx.this)
    inputReserve = basetoken.balance_of(ctx.this)
    basetoken.transfer_from(amount, ctx.this, fromAddress)
    assert inputReserve > 0 and outputReserve > 0
    numerator = amount * outputReserve
    denominator = (inputReserve) + amount
    amount = (numerator / denominator)
    currency.transfer(amount, fromAddress)
@export
def addLiquidity(amountInTAU:int):
    assert amountInTAU > 0, 'Cannot add negative liquidity'
    tokenReserve = basetoken.balance_of(ctx.this)
    TAUReserve = currency.balance_of(ctx.this)
    basetoken.transfer_from((amountInTAU * basetoken.balance_of(ctx.this) / currency.balance_of(ctx.this)), ctx.this, ctx.caller)
    currency.transfer_from(amountInTAU, ctx.this, ctx.caller)
    tokenWorthInTAU = TAUReserve / totalLiquidityTokens[ctx.this]
    tokenAmount = amountInTAU / tokenWorthInTAU
    liquidityTokenBalance[ctx.caller] += tokenAmount
    totalLiquidityTokens[ctx.this] += tokenAmount
    return tokenAmount 
@export
def removeLiquidity(amount: int):
    assert amount > 0, 'Cannot add negative liquidity'
    assert liquidityTokenBalance[ctx.caller] >= amount, 'Not enough liquidity tokens'
    liquidityTokenBalance[ctx.caller] -= amount
    percentOfPool = amount / totalLiquidityTokens[ctx.this]
    totalLiquidityTokens[ctx.this] -= amount
    TAUPayout = currency.balance_of(ctx.this) * percentOfPool
    tokenPayout = basetoken.balance_of(ctx.this) * percentOfPool
    assert tokenPayout > 0 
    assert TAUPayout > 0
    assert TAUPayout < currency.balance_of(ctx.this)
    assert tokenPayout < basetoken.balance_of(ctx.this)
    currency.transfer(TAUPayout, ctx.caller)
    basetoken.transfer(tokenPayout, ctx.caller)
    return TAUPayout, tokenPayout
@export
def transfer(amount: int, receiver: str):
    #transfer liquidity token
    assert amount > 0, 'Cannot send negative balance'
    sender = ctx.caller
    balance = liquidityTokenBalance[sender]
    assert balance >= amount, "Transfer amount exceeds available balance"
    liquidityTokenBalance[sender] -= amount
    liquidityTokenBalance[receiver] += amount
@export
def liquidityRatio():
    tokenReserve = basetoken.balance_of(ctx.this)
    TAUReserve = currency.balance_of(ctx.this)
    return TAUReserve, tokenReserve
    return TAUReserve / tokenReserve""".format(tokenAddress,tokenAddress,tokenAddress,tokenAddress,tokenAddress,tokenAddress,tokenAddress,tokenAddress,tokenAddress,tokenAddress,tokenAddress)
    submission.submit_contract(AMMAddress, contract)
    exchangeList = allExchanges.get()
    allExchanges.set(exchangeList + "\n" + AMMAddress)
@export
def setGovernenceToken(address: str):
    assert ctx.owner == ctx.caller
    assert disableChangingContract.get() == 0
    governenceContract.set(address)
@export
def disableContractChanges():
    assert ctx.owner == ctx.caller
    disableChangingContract.set(1)
@export
def forwardTransactionFeeRewards():
    assert disableChangingContract.get() == 1
    amount = currency.balance_of(ctx.this)
    currency.transfer(amount, governenceContract.get())
    
   
    

