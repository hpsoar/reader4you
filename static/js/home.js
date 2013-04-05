$(function() {
    var util = {
      addFeed: function() {
        $.getJSON($SCRIPT_ROOT + '/add_feed', {
          feed_url: $('#feed_url').val()
        }, function(data) {
          if (data.state == 'ok') {
            util.addToFeedList(data.feed);
            util.showArticles(data.feed, data.stories)
          }
          else if (data.state == 'duplication') {
            alert('already added!');
          }
          else {
            alert('error');
          }
          $('#feed_url').val('');
        });
      },
      clearArticles: function() {
        $('#itemlist').html('');
      },
      itemView: function(item) {
        // TODO: find all in ${}, replace with corresponding field in item
        // create document node
      },
      itemHtml: '<div class=article_summary_view>' +
                  '<div class=title>' + 
                      '<a class=link href=${link} >${title}</a>' +
                      '<span class=pubdate>${publish_date}</span>' +
                  '</div>' +
                  '<div class=author>${author}</div>' +
                  '<div>${summary}</div>' + 
                '</div>',
      addArticle: function(item) {
        // TODO: use a template
        $(util.itemHtml.replace('${title}', item.title)
                       .replace('${link}', item.link)
                       .replace('${publish_date}', item.publish_date)
                       .replace('${author}', item.author)
                       .replace('${summary}', item.summary))
        .appendTo($('#itemlist'));
      },
      showArticles: function(feed, items) {
        util.clearArticles();
        $('#feedtitle').attr('href', feed.link);
        $('#feedtitle').html(feed.feed_title);
        $.each(items, function(index, item) {
          util.addArticle(item);
        });
      },
      getArticles: function(feed) {
        $.getJSON($SCRIPT_ROOT + '/get_stories', {
          feed_id: feed.feed_id
        }, function(data) {
          util.showArticles(feed, data.stories);
        });
      },
      selectedFeed:null,
      addToFeedList: function(feed) {
        $('<a>',{
          text: feed.feed_title,
          href: feed.feed_link,
          class: 'feedItem',
        }).appendTo($('<li>').click(function() {
           util.selectFeed(feed, $(this)); 
           return false;
        }).appendTo($('#feedlist')));
      },
      selectFeed: function(feed, obj) {
        util.getArticles(feed);
        if (util.selectedFeed) {
          util.selectedFeed.removeClass('active');
        }
        console.log(obj);
        obj.addClass('active');
        util.selectedFeed = obj;
      },
      getFeedList: function() {
        $.getJSON($SCRIPT_ROOT + '/get_feedlist', {
        }, function(data) {
          $.each(data.feedlist, function(index, feed){
            util.addToFeedList(feed);
          });
          if (data.feedlist.length > 0) {
            util.selectFeed(data.feedlist[0], $('#feedlist li:first-child'));
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

