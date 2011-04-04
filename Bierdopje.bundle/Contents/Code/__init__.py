NAME = 'Bierdopje'

API_URL = 'http://api.bierdopje.com/' + Prefs['ApiKey'] + '/'
SHOW_URL = API_URL + 'GetShowByTVDBID/%s'
SUBTITLE_URL = API_URL + 'GetAllSubsFor/%s/%s/%s/nl'

def Start():
  HTTP.CacheTime = CACHE_1HOUR

class BierdopjeAgentTV(Agent.TV_Shows):
  name = 'Bierdopje'
  languages = [Locale.Language.Dutch]
  primary_provider = False
  contributes_to = ['com.plexapp.agents.thetvdb']

  def search(self, results, media, lang):
    Log('*** Trying to find a match for TVDBID %s' % media.primary_metadata.id)
    bierdopje_id = XML.ElementFromURL(SHOW_URL % media.primary_metadata.id).xpath('/bierdopje/response/showid')[0].text
    Log('*** Bierdopje id: %s' % bierdopje_id)
    results.Append(MetadataSearchResult(
      id    = bierdopje_id,
      score = 100
    ))

  def update(self, metadata, media, lang):
    HTTP.Headers['User-agent'] = 'plexapp.com v9.0'
    for s in media.seasons:
      # just like in the Local Media Agent, if we have a date-based season skip for now.
      if int(s) < 1900:
        for e in media.seasons[s].episodes:
          for i in media.seasons[s].episodes[e].items:
            for p in i.parts:
              subtitles = XML.ElementFromURL(SUBTITLE_URL % (metadata.id, s, e)).xpath('/bierdopje/response/results/result')
              match = None
              if len(subtitles) > 0:
                for subtitle in subtitles:
                  filename = subtitle.xpath('filename')[0].text
                  Log('*** Subtitle found on bierdopje: %s' % filename)
                  if p.file.lower().find(filename.lower()) != -1:
                    match = subtitle
                    Log('*** We found a match: %s' % filename)
                    break
                if match:
                  Log('*** Will use this subtitle: %s' % match.xpath('filename')[0].text)
                  download_link = match.xpath('downloadlink')[0].text
                  Log('*** Download url: %s' % download_link)
                  # We use the .srt extension by default. There is no way to see what we get back from the api.
                  p.subtitles[Locale.Language.Dutch][download_link] = Proxy.Media(HTTP.Request(download_link), ext='srt')
                else:
                  Log('*** No exact match found. Will try the most popular one now.')
                  Log('*** TODO: Of course this should be implemented')
              else:
                Log('*** No subtitles found on bierdopje')
