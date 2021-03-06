import re

API_URL = 'http://api.bierdopje.com/%s' % Prefs['ApiKey']
SHOW_URL = '%s/GetShowByTVDBID/%%s' % API_URL
SUBTITLE_URL = '%s/GetAllSubsFor/%%s/%%s/%%s/%%s/' % API_URL

FORMAT_REGEXP = re.compile(r'(sdtv|pdtv|hdtv|web-dl|dvdscr|dvdrip|dvdr|bluray)', re.IGNORECASE)
ENCODING_REGEXP = re.compile(r'(pal|ntsc|divx|xvid|x264)', re.IGNORECASE)
RESOLUTION_REGEXP = re.compile(r'((240|480|720|1080)[i|p])', re.IGNORECASE)

def Start():
  HTTP.CacheTime = CACHE_1HOUR
  HTTP.Headers['User-agent'] = 'plexapp.com v9.0'

class BierdopjeAgentTV(Agent.TV_Shows):
  name = 'Bierdopje'
  languages = [Locale.Language.Dutch, Locale.Language.English]
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
    for season in media.seasons:
      # just like in the Local Media Agent, if we have a date-based season skip for now.
      if int(season) < 1900:
        for episode in media.seasons[season].episodes:
          for item in media.seasons[season].episodes[episode].items:
            for part in item.parts:
              if Prefs['Language'] == 'both':
                for language in ['nl', 'en']:
                  self.find(metadata, season, episode, part, language)
              else:
                self.find(metadata, season, episode, part, Prefs['Language'])

  def find(self, metadata, season, episode, part, language):
    subtitles = XML.ElementFromURL(SUBTITLE_URL % (metadata.id, season, episode, language), sleep=1.0).xpath('/bierdopje/response/results/result')
    match = None
    if len(subtitles) > 0:
      for subtitle in subtitles:
        filename = subtitle.xpath('filename')[0].text
        Log('*** Subtitle found on bierdopje: %s' % filename)
        if part.file.lower().find(filename.lower().replace('.srt', '')) != -1:
          match = subtitle
          Log('*** We found a match: %s' % filename)
          break
      if match:
        self.fetch(part, match, language)
      else:
        match = self.find_best_match(part.file, subtitles)
        if match:
          self.fetch(part, match, language)
        elif Prefs['DownloadMostPopular']:
          Log('*** No exact match found. Will try the most popular one now.')
          match = sorted(subtitles, key=lambda subtitle: int(subtitle.xpath('numdownloads')[0].text))[-1]
          self.fetch(part, match, language)
        else:
          Log('*** No matches found on bierdopje. You might check the preferences to enable more generous checking.')
    else:
      Log('*** No subtitles found on bierdopje')

  def find_best_match(self, filename, subtitles):
    Log('*** Trying to find the best match')
    filename_matches = self.regexp_matches(filename.replace(' ', ''))
    points = {'formats': 4, 'encodings': 2, 'resolutions': 1}
    scores = []
    for subtitle in subtitles:
      bd_filename = subtitle.xpath('filename')[0].text
      score = 0
      for key, value in self.regexp_matches(bd_filename).iteritems():
        if (filename_matches[key] and value and filename_matches[key] == value):
          score += points[key]
      if score > 0:
        scores.append({'subtitle': subtitle, 'score': score})
      else:
        Log('*** No good matches found')
    if scores:
      match = sorted(scores, key=lambda regexp_match: regexp_match['score'])[-1]
      Log('*** Found the best match with %i points' % match['score'])
      return match['subtitle']

  def regexp_matches(self, filename):
    return {'formats': FORMAT_REGEXP.findall(filename), 'encodings': ENCODING_REGEXP.findall(filename), 'resolutions': RESOLUTION_REGEXP.findall(filename)}

  def fetch(self, part, subtitle, language):
    Log('*** We will use this subtitle: %s' % subtitle.xpath('filename')[0].text)
    download_link = subtitle.xpath('downloadlink')[0].text
    key = download_link.split('/apikey/')[0]
    request = HTTP.Request(download_link, cacheTime=CACHE_1MONTH)
    try:
      ext = re.search('^attachment; filename=.*\.(.+?)$', request.headers['content-disposition']).group(1)
      Log('*** Found extension %s' % ext)
    except:
      ext = 'srt'
      Log('*** Couldn\'t figure out the file extension, we will use srt.')
    part.subtitles[language][key] = Proxy.Media(request, ext=ext)
