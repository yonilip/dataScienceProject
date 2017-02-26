// Copyright (c) 2012 The Chromium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// Event listener for clicks on links in a browser action popup.
// Open the link in a new tab of the current window.
function onAnchorClick(event) {
  chrome.tabs.create({
    selected: true,
    url: event.srcElement.href
  });
  return false;
}


function readData() {
    alert("done");
}
// Given an array of timestamps and URLs, build a DOM table in the
// browser action popup.
function buildPopupDom(tableName, data) {
    chrome.storage.sync.get(['foo', 'bar'], function(items) {
        message('Settings retrieved', items);
    })
  var table = document.getElementById(tableName);
  for (var i = 0, ie = 9; i < ie; ++i) {
    var tr = document.createElement('tr');
    table.appendChild(tr);
  
    // var date = new Date( data[i][0] );
    // var dateString =
    //     // padZero(date.getHours()) + ':' +
    //     // padZero(date.getMinutes()) + ':' +
    //     // padZero(date.getSeconds()) + '.' +
    //     // padZero(date.getMilliseconds(),3)
    //     ie
    // ;
   
    // var timeTd = document.createElement('td');
    // tr.appendChild(timeTd);
    // var timeText = document.createTextNode( dateString );
    // timeTd.appendChild(timeText);

    var urlTd = document.createElement('td');
    tr.appendChild(urlTd);
    var urlText = document.createTextNode( data[i][1] );
    urlTd.appendChild(urlText);
  }
}


// Shows recently visited urls in a popup
function buildVisitedUrlList(divName) {
  var fiveMinutesAgo = (new Date).getTime() - 1000 * 60 * 5;

  // Track the number of callbacks from chrome.history.getVisits()
  // that we expect to get.  When it reaches zero, we have all results.
  var numRequestsOutstanding = 0;

  chrome.history.search({
      'text': '',                 // Return every history item....
      'startTime': fiveMinutesAgo,
      'maxResults': 10000
    },
    function(historyItems) {
      // For each history item, get details on all visits.
      for (var i = 0; i < historyItems.length; ++i) {
        var url = historyItems[i].url;
        var processVisitsWithUrl = function(url) {
          // We need the url of the visited item to process the visit.
          // Use a closure to bind the  url into the callback's args.
          return function(visitItems) {
            processVisits(url, visitItems);
          };
        };
        chrome.history.getVisits({url: url}, processVisitsWithUrl(url));
        numRequestsOutstanding++;
      }
      if (!numRequestsOutstanding) {
        onAllVisitsProcessed();
      }
    });


  var visits = [];

  // Callback for chrome.history.getVisits().  Counts the number of
  // times a user visited a URL by typing the address.
  var processVisits = function(url, visitItems) {
    for (var i = 0, ie = visitItems.length; i < ie; ++i) {
      var visitTime = visitItems[i].visitTime;
      if (visitTime > fiveMinutesAgo) {
        visits.push( [ visitTime, url ] );
      }
    }

    // If this is the final outstanding call to processVisits(),
    // then we have the final results.  Use them to build the list
    // of URLs to show in the popup.
    if (!--numRequestsOutstanding) {
      onAllVisitsProcessed();
    }
  };

  // This function is called when we have the final list of Urls to display.
  var onAllVisitsProcessed = function() {
    // Sort the visits array
    visits.sort(function(a, b) {
      return b[0] - a[0];
    });

    buildPopupDom(divName, visits);
  };
}

function padZero(number, length) {
    var numString = number.toString();
    var zero = '0';
    length = length || 2;

    while(numString.length < length) {
        numString = zero + numString;
    }

    return numString;
}

document.addEventListener('DOMContentLoaded', function () {
  buildVisitedUrlList("visitedUrls");
});
