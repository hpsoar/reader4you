$(function() {
    var util = {
      addFeed: function() {
        $.getJSON($SCRIPT_ROOT + '/add_feed', {
          feed_url: $('#feed_url').val()
        }, function(data) {
          if (data) {
            util.addToFeedList(data);
            util.showItems(data.title, data.articles)
          }
          else {
            alert('error')
          }
          $('#feed_url').val('');
        });
      },
      clearItems: function() {
        $('#itemlist').html('');
      },
      itemHtml: '<div><div><h4>${title}</h4></div>' +
                  '<div>${author, date...}</div>' +
                '<div>${description}</div></div>',
      addItem: function(item) {
        // use a template
        var itemView = $(util.itemHtml.replace('${title}', item.title)
                .replace('${description}', item.description));
        itemView.attr('class', 'article_summary0');
        itemView.appendTo($('#itemlist'));
      },
      showItems: function(title, items) {
        util.clearItems();
        $('#feedtitle').html(title);
        $.each(items, function(index, item) {
          util.addItem(item);
        });
      },
      addToFeedList: function(feed) {
        $('<a>',{
          text: feed.title,
          href: feed.link,
          class: 'feedItem',
          click: function(){ 
            $.getJSON($SCRIPT_ROOT + '/get_articles', {
              feed_id: feed.id
            }, function(data) {
              util.showItems(feed.title, data.articles);
            });
            return false;
          }
        }).appendTo($('<li>').appendTo($('#feedlist')));
      },
      getFeedList: function() {
        $.getJSON($SCRIPT_ROOT + '/get_feedlist', {
        }, function(data) {
          $.each(data.feedlist, function(index, feed){
            util.addToFeedList(feed);
          });
          if (data.feedlist.length > 0) {
            util.showItems(data.feedlist[0].title, data.articles);
          }
        });
      },
      keyPressed: function(e) {
        var code = (e.keyCode ? e.keyCode : e.which);
        if (code == 13) {
          util.addFeed();
        }
      }
    };

  $('#feed_url').bind('keypress', util.keyPressed);
  util.getFeedList();
});

