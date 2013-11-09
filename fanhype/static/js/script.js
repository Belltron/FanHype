/* Script for CSCE 470 search engine
 *
 */

var tweet_template = _.template($('#tweet_template').html(),null,{variable:'t'});
var result_template = _.template($('#result_template').html());
var alert_template = _.template($('#alert_template').html());

$(function() {
  ajax_search("...");
  setInterval(function(){
    ajax_search("...");
  },5000);
  
});

function ajax_search(q) {
  $.ajax('/search',{
      data:{q:q},
      timeout:15000,
      success: function(data) {
        mapNewTweet(data.tweets);
      },
      error: function(jqXHR,textStatus,errorThrown) {
        
        console.log("Could not connect to the server");
      },
      dataType: 'json',
  });
}

