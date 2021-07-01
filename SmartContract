// edwcoins ICO

// Version of compiler

pragma solidity ^0.4.11; 

contract hadcoin_ico {
    // introducint the maximum number of edwcoins available for sealed
    uint public max_edwcoins = 1000000; 
    
    // Introfucint the USD to edwcoins conversion rate 
    uint public usd_to_edwcoins = 1000; 
    
    // Introducing the total number of edwcoins that have been bought by the investors
    uint public total_edwcoins_bought = 0; // beginning of the ico no one has bought it 
    
    // Mapping from the investor address to its equity in edwcoins and USD 
    mapping(address => uint) equity_edwcoins; 
    mapping(address => uint) equity_usd; 
    
    // Checking if an investor can buy edwcoins
    modifier can_buy_edwcoins(uint usd_invested) {
        require (usd_invested * usd_to_edwcoins + total_edwcoins_bought <= max_edwcoins); 
        _; 
    }
    
    // Getting the equity in edwcoins of an investor, external means out side of contract
    function equity_in_edwcoins(address investor) external constant returns (uint) {
       return equity_in_edwcoins[investor]; 
    }
    
    // Getting the equity in USD of an investor
    function equity_in_usd(address investor) external constant returns (uint) {
       return equity_usd[investor]; 
    }
    
    // Buying edwcoins
    function buy_edwcoins(address investor, uint usd_invested) external 
    can_buy_edwcoins(usd_invested) {
        uint edwcoins_bought = usd_invested * usd_to_edwcoins; 
        
        // current investor
        equity_edwcoins[investor] += edwcoins_bought; 
        equity_usd[investor] = equity_edwcoins[investor] / usd_to_edwcoins; 
        total_edwcoins_bought += edwcoins_bought;
        
    }
    
    // Selling edwcoins
    function sell_edwcoins(address investor, uint edwcoins_to_sell) external {
        uint edwcoins_bought = usd_invested * usd_to_edwcoins; 
        // current investor
        equity_edwcoins[investor] -= edwcoins_bought; 
        equity_usd[investor] = equity_edwcoins[investor] / usd_to_edwcoins; 
        total_edwcoins_bought -= edwcoins_to_sell;

    }
    
}    
    
    
}
