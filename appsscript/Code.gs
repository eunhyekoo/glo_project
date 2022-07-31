async function getTapasClientRegistryData() {
  allSheets = SpreadsheetApp.openById(CLIENT_REGISTRY_SHEETS_ID).getSheets();

  var idx = 0;
  // idx = 타파스 탭 위치 
  for (i = 0; i<allSheets.length; i++){
    if (allSheets[i].getName() == 'Tapas'){
      idx= i
    }
  }
  let tapasSheet = allSheets[idx]

  let oneTitle = tapasSheet.getName();
  let data = tapasSheet.getDataRange().getValues();
  let gid = tapasSheet.getSheetId(); // get gid
  let columnName = data[0].slice(0,15);
  let customColumnName = ['title', 'feedbackDate', 'type', 'category','subcategory1', 'subcategory2', 'feedbackComments', 'sentimentLevel', 'severityLevel', 'episodeNumber','sourceLanguage', 'targetLanguage','isRrated'];
  //Logger.log(columnName)

  allFeedbackData = data.slice(1, -1).map((oneFeedback) => {
    oneTitleData = {};
    oneFeedbackData = oneFeedback.slice(0, 13);
    customColumnName.forEach((key, value) => oneTitleData[key] = oneFeedbackData[value].toString());
    //Logger.log(oneTitleData)
    // add sheetId, gid
    oneTitleData['sheetId'] = CLIENT_REGISTRY_SHEETS_ID; 
    oneTitleData['gid'] = gid.toString();

    // add client
    oneTitleData['client'] = 'Tapas'
    console.log(oneTitleData);
    return oneTitleData;
  })
  await callApi(allFeedbackData);
}

//TODO : API 연결
function callApi(allFeedbackData) {
  console.log(allFeedbackData);
  const url = SAVING_FEEDBACK_API_ENDPOINT;
    
  for (oneClientRegistry of allFeedbackData) {
    let options = {
      'method' : 'post',
      'accept' : 'application/json',
      'Content-Type': 'application/json',
      // Convert the JavaScript object to a JSON string.
      'payload' : oneClientRegistry
      };
    
    try {
      response = UrlFetchApp.fetch(url, options);
      // Logger.log(response.getContentText());
      console.log(response.getResponseCode()); // 201 created 
      // console.log(response.getContentText());
    } catch(e) {
      console.log(e);
      console.log('데이터 저장에 실패하였습니다.')
      console.log(oneClientRegistry);
      continue;
    }
  }
}

/**
 create trigger(Run only once)
 */
function sheetChangeTrigger(){
  let sheet = SpreadsheetApp.openById(CLIENT_REGISTRY_SHEETS_ID);
  ScriptApp.newTrigger("checkProperty")
    .forSpreadsheet(sheet)
    .onChange()
    .create();
}
/** 
function checkProperty() {
    const url = SAVING_FEEDBACK_API_ENDPOINT;
    getKKEClientRegistryData();
}
*/