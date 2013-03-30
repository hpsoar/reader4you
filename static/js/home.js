$(function() {
    var util = {
      addFeed: function() {
        $.getJSON($SCRIPT_ROOT + '/add_feed', {
          feed_url: $('#feed_url').val()
        }, function(data) {
          if (data.state == 'ok') {
            util.addToFeedList(data.feed);
            util.showArticles(data.feed, data.articles)
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
                      '<span class=pubdate>${published}</span>' +
                  '</div>' +
                  '<div class=author>${author}</div>' +
                  '<div>${description}</div>' + 
                '</div>',
      addArticle: function(item) {
        // TODO: use a template
        $(util.itemHtml.replace('${title}', item.title)
                       .replace('${link}', item.link)
                       .replace('${published}', item.published_parsed)
                       .replace('${author}', item.author)
                       .replace('${description}', item.description))
        .appendTo($('#itemlist'));
      },
      showArticles: function(feed, items) {
        util.clearArticles();
        $('#feedtitle').attr('href', feed.link).html(feed.title);
        $.each(items, function(index, item) {
          util.addArticle(item);
        });
      },
      getArticles: function(feed) {
        $.getJSON($SCRIPT_ROOT + '/get_articles', {
          feed_id: feed.id
        }, function(data) {
          util.showArticles(feed, data.articles);
        });
      },
      addToFeedList: function(feed) {
        $('<a>',{
          text: feed.title,
          href: feed.link,
          class: 'feedItem',
          click: function(){ 
            util.getArticles(feed);
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
            console.log(data.feedlist);
            util.getArticles(data.feedlist[0]);
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

