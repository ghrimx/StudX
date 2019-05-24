
// Source: http://jsfiddle.net/BSeN6/2/

function TimeDiff(a,b)
{  
    var first = a.split(":")
    var second = b.split(":")
        
        var xx;
        var yy;
        
        if(parseInt(first[0]) < parseInt(second[0])){          
            
            if(parseInt(first[1]) < parseInt(second[1])){
                
                yy = parseInt(first[1]) + 60 - parseInt(second[1]);
                xx = parseInt(first[0]) + 24 - 1 - parseInt(second[0])
            
            }else{
              yy = parseInt(first[1]) - parseInt(second[1]);
              xx = parseInt(first[0]) + 24 - parseInt(second[0])
            }

        }else if(parseInt(first[0]) == parseInt(second[0])){
        
          if(parseInt(first[1]) < parseInt(second[1])){
                
                yy = parseInt(first[1]) + 60 - parseInt(second[1]);
                xx = parseInt(first[0]) + 24 - 1 - parseInt(second[0])
            
            }else{
              yy = parseInt(first[1]) - parseInt(second[1]);
              xx = parseInt(first[0]) - parseInt(second[0])
            }
        
        }else{
            
          if(parseInt(first[1]) < parseInt(second[1])){
                
                yy = parseInt(first[1]) + 60 - parseInt(second[1]);
                xx = parseInt(first[0]) - 1 - parseInt(second[0])
            
            }else{
              yy = parseInt(first[1]) - parseInt(second[1]);
              xx = parseInt(first[0]) - parseInt(second[0])
            }
        }
    
    if(xx < 10)
        xx = "0" + xx
          
    if(yy < 10)
        yy = "0" + yy
  
    return(xx + ":" + yy)  
};
