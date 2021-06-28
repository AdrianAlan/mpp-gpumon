'use strict'
const config = require('./config')
const fetch = require('node-fetch')
const { WebClient } = require('@slack/web-api')
const { createEventAdapter } = require('@slack/events-api')

const slackSigningSecret = '';
const slackToken = '';
const slackEvents = createEventAdapter(slackSigningSecret);
const slackClient = new WebClient(slackToken);

var mppGPUs = ['all', 'mpp-tatooine', 'naboo', 'mustafar', 'kamino', 'geonosis', 'dagobah'];

function sendMessage(channelId, outText) {
  (async () => {
    try {
      await slackClient.chat.postMessage({
        channel: channelId,
        text: outText});
    } catch (error) {
      console.log(error.data);
    }
  })();
};

function isValidGPU(gpuList) {
  for (var i=0; i<gpuList.length; i++) {
    if (mppGPUs.includes(gpuList[i])) {
      return true;
    }
  }
  return false;
}

slackEvents.on('message', (event) => {
  if (event.text.toLowerCase().startsWith("status")) {
    var request = event.text.split(" ");
    var gpuList = request.slice(1, request.length);
    console.log(gpuList);
    if (isValidGPU(gpuList)) {
      (async () => {
	try {
          await fetch('https://gitlab.cern.ch/adpol/mpp-gpumon/-/raw/master/status.json')
          .then((response) => response.json())
          .then((json) => {
            if (gpuList.includes('all')) {
              gpuList = mppGPUs.slice(1, mppGPUs.length);
            }
            for (var i=0; i<gpuList.length; i++) {
              for(var j=0; j<json.length; j++){
                if (json[j]["name"] === gpuList[i]) {
                  var details = json[j]["details"];
	          for(var k=0; k<details.length; k++) {
                    var whoisin = details[k]['users'];
                    if (whoisin) {
                      var ext = ' is occupied by ' + whoisin;
                    } else {
                      var ext = ' is FREE! :tada:';
                    }
                    sendMessage(`@${event.user}`, gpuList[i] + "'s GPU " + details[k]['_id'] + ext);
                  }
                }
              }
            }
	   })
         } catch(error) {
	   console.log(error.data);
         }
       })();
    } else {
      sendMessage(`@${event.user}`, 'I only know about these GPUs: ' + mppGPUs.join(', '));
    }
  }
});

slackEvents.on('app_mention', (event) => {
  (async () => {
    try {
      await slackClient.chat.postMessage({ channel: `@${event.user}`, text: `Hello <@${event.user}>! Ask me about GPUs! :tada:`});
    } catch (error) {
      console.log(error.data);
    }
 })();
});

// Error Handler
slackEvents.on('error', console.error);

slackEvents.start(config('PORT')).then(() => {
  console.log('Server started')
});
