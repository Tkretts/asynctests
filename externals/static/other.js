/**
 * Created by as.bogunkov on 05.11.2015.
 */

$(document).ready(function(){
   pushMeConnection.subscribe(function(msg, topic){
      if (topic == 'send-message' && !!msg && msg != '') {
         alert(msg);
      }
   });
});