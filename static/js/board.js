
$(function() {
    //alert('js start');
    var counter = 1; 
    var timer;
    var dtS = Date.now();
    var maxN =  $(".field").size();


   
   function zeroPad(num, places) {
 	 var zero = places - num.toString().length + 1;
  	return Array(+(zero > 0 && zero)).join("0") + num;
   }

   function scoreToString(score){
     var mi = Math.floor(score/60000);
     var s = Math.floor((score - mi*60000)/1000);
     return zeroPad(mi, 2)+ ':' + zeroPad(s, 2) + '.' + zeroPad((score%1000), 3);
   }
    
    function msToString(){
      dtF = Date.now();
      ms = dtF - dtS
      return ms;
    }

    function win(time){
       //location.href = '../champion?'+'time='+time;
       $.post("../settime", { time: time },
 	 	function(data){
  	});
        location.href = '../champion'
    }
    
   
    $('.field').click(function() {
 
    clicknum = $(this).text();
    alerttext = 'loose';
    if (clicknum==counter){
	alerttext = msToString();        
 	
	//alerttext = 'ok';
        if (counter == maxN){
          win(alerttext);
          return;
        }
        counter +=1;
        b = $('#hint');
        b.text(counter);
        //alert(b);
    }
    //alert(alerttext+'_____'+counter);

    });

   
    $('.score-cell').each(function() {
  	a = $( this );

        var b = parseInt(a.text());
        a.text(scoreToString(b));
     });

   function setSubmitActive(flag) {
	a = $('input[type=submit]');
        if (flag)
		a.removeAttr('disabled');
	else
        	a.attr('disabled','disabled');


   }

   $('input[name="champion_name"]').bind('input', function(){
        inp = $(this).val();
        inp = inp.trim();
        setSubmitActive(inp.length>0);
        //attr('disabled','disabled');
	
   })

   setSubmitActive(false);
   
});


