function OnStableStudy(studyId, tags, metadata)

    -- debug
    PrintRecursive('Загружено новое исследование: ' .. studyId)
  
    Отправка нового стабильного исследования в облако
    local body = '{\"Resources\":[{\"Level\":\"Study\",\"ID\":\"' .. studyId .. '\"}],\"Compression\":\"gzip\",\"Peer\":\"cloud-ro-pacs\"}'
    RestApiPost('/transfers/send', body)
    PrintRecursive('Исследование отправлено в облако')
  
    -- Удаление исследования на remote
    -- RestApiDelete('/studies/' .. studyId)
  end