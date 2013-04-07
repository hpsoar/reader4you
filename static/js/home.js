$(function() {
    var view = {
      addFeed: function() {
        $.getJSON($SCRIPT_ROOT + '/add_feed', {
          feed_url: $('#feed_url').val()
        }, function(data) {
          if (data.state == 'ok') {
            view.addToFeedList(data.feed);
            view.showArticles(data.feed, data.stories)
            view.showFeedSelection($('#feedlist li:last-child'));

            // scroll to added feed
            $('#feedlist_container')[0].scrollTop = divObj.scrollHeight;
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
      itemHtml: '<div class=article_summary_view>' +
                  '<div class=title>' + 
                      '<a class=link href=${link} >${title}</a>' +
                      '<span class=pubdate>${publish_date}</span>' +
                  '</div>' +
                  '<div class=author>${author}</div>' +
                  '<div>${summary}</div>' + 
                '</div>',
      showArticles: function(feed, items) {
        if (feed != view.selectedFeed) {
          view.selectedFeed = feed;
          view.storyList.html('');
        }

        $('#feedtitle').attr('href', feed.link);
        $('#feedtitle').html(feed.feed_title);

        $.each(items, function(index, item) {
          util.applyTmpl(view.itemHtml, item).appendTo(view.storyList);
        });
        console.log($('#itemlist').children('div').length);
      },
      pageIdx: 0,
      pageSize: 6,
      fetching: false,
      selectedFeed: null,
      selectedFeedItem:null,
      storyList: $('#itemlist'),
      getArticles: function(feed) {
        if (view.fetching) return;
        view.fetching = true;

        $.getJSON($SCRIPT_ROOT + '/get_stories', {
          feed_id: feed.feed_id,
          page:view.pageIdx,
          limit:view.pageSize,
        }, function(data) {
          view.showArticles(feed, data.stories);
          if (data.stories.length > 0) { 
            ++view.pageIdx;
          }
          else {
            console.log(view.pageIdx + '; ' + data.stories.length);
            console.log('no more');
          }
        }).always(function() {
          view.fetching = false;
        });
      },
      showFeedSelection:function(obj) {
        if (view.selectedFeedItem) {
          view.selectedFeedItem.removeClass('active');
        }
        obj.addClass('active');
        view.selectedFeedItem = obj;
      },
      addToFeedList: function(feed) {
        $('<a>',{
          text: feed.feed_title,
          href: feed.feed_link,
          class: 'feedItem',
        }).appendTo($('<li>').click(function() {
          view.getArticles(feed);
          view.showFeedSelection($(this));
          return false;
        }).appendTo($('#feedlist')));
      },
      getFeedList: function() {
        $.getJSON($SCRIPT_ROOT + '/get_feedlist', {
          'story_for_feed': 0,
        }, function(data) {
          $.each(data.feedlist, function(index, feed){
            view.addToFeedList(feed);
          });
          if (data.feedlist.length > 0) {
            view.getArticles(data.feedlist[0]); 
            view.showFeedSelection($('#feedlist li:first-child'));
          }
        });
      },
      keyPressed: function(e) {
        var code = (e.keyCode ? e.keyCode : e.which);
        if (code == 13) {
          view.addFeed();
        }
      }
    };

  $('#feed_url').bind('keypress', view.keyPressed);
  $('#content-area').scroll(function(event) {
    var storyItems = view.storyList.children('div');
    if (storyItems.length < view.limit) return;
    var checkPoint = storyItems.eq(Math.max(storyItems.length - 2, 0)).offset().top;
    var pivotal = $('#content-area').scrollTop() + $('#content-area').height();
    // TODO: fix bug for too short list
    if (pivotal > checkPoint) view.getArticles(view.selectedFeed);
  });
  view.getFeedList();
});

