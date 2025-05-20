-- Tüm maçları listele
SELECT * FROM matches LIMIT 5;

-- Sezonlara göre toplam maç sayısı
SELECT Season, COUNT(*) as match_count 
FROM matches 
GROUP BY Season 
ORDER BY Season;

-- En çok gol atan maçlar
SELECT Season, MatchDate, HomeTeam, AwayTeam, 
       FullTimeHomeGoals, FullTimeAwayGoals,
       (FullTimeHomeGoals + FullTimeAwayGoals) as total_goals
FROM matches
ORDER BY total_goals DESC
LIMIT 10;

-- Takımların ev sahibi olarak kazandığı maç sayısı
SELECT HomeTeam, COUNT(*) as home_wins
FROM matches
WHERE FullTimeResult = 'H'
GROUP BY HomeTeam
ORDER BY home_wins DESC;

-- En çok kırmızı kart gören takımlar
SELECT HomeTeam as Team, SUM(HomeRedCards) as HomeRedCards,
       SUM(AwayRedCards) as AwayRedCards,
       (SUM(HomeRedCards) + SUM(AwayRedCards)) as TotalRedCards
FROM matches
GROUP BY HomeTeam
ORDER BY TotalRedCards DESC
LIMIT 10;

-- Sezonlara göre ortalama gol sayısı
SELECT Season, 
       AVG(FullTimeHomeGoals + FullTimeAwayGoals) as avg_goals_per_match
FROM matches
GROUP BY Season
ORDER BY Season;

-- Takımların sezonlara göre performans analizi
SELECT 
    Season,
    HomeTeam as Team,
    COUNT(*) as total_matches,
    SUM(CASE WHEN FullTimeResult = 'H' THEN 1 ELSE 0 END) as wins,
    SUM(CASE WHEN FullTimeResult = 'D' THEN 1 ELSE 0 END) as draws,
    SUM(CASE WHEN FullTimeResult = 'A' THEN 1 ELSE 0 END) as losses,
    SUM(FullTimeHomeGoals) as goals_scored,
    SUM(FullTimeAwayGoals) as goals_conceded,
    SUM(FullTimeHomeGoals - FullTimeAwayGoals) as goal_difference
FROM matches
GROUP BY Season, HomeTeam
ORDER BY Season, goal_difference DESC
LIMIT 20;

-- En çok şut çeken ve isabetli şut atan takımlar
SELECT 
    HomeTeam as Team,
    AVG(HomeShots) as avg_shots_per_game,
    AVG(HomeShotsOnTarget) as avg_shots_on_target,
    ROUND(AVG(HomeShotsOnTarget) * 100.0 / NULLIF(AVG(HomeShots), 0), 2) as shot_accuracy
FROM matches
GROUP BY HomeTeam
HAVING avg_shots_per_game > 0
ORDER BY shot_accuracy DESC
LIMIT 10;

-- En agresif takımlar (faul ve kart istatistikleri)
SELECT 
    HomeTeam as Team,
    AVG(HomeFouls) as avg_fouls_per_game,
    AVG(HomeYellowCards) as avg_yellow_cards,
    AVG(HomeRedCards) as avg_red_cards,
    (AVG(HomeYellowCards) + AVG(HomeRedCards) * 2) as discipline_score
FROM matches
GROUP BY HomeTeam
ORDER BY discipline_score DESC
LIMIT 10;

-- İlk yarı ve ikinci yarı performans karşılaştırması
SELECT 
    HomeTeam as Team,
    AVG(HalfTimeHomeGoals) as avg_first_half_goals,
    AVG(FullTimeHomeGoals - HalfTimeHomeGoals) as avg_second_half_goals,
    AVG(FullTimeHomeGoals) as avg_total_goals
FROM matches
GROUP BY HomeTeam
ORDER BY avg_total_goals DESC
LIMIT 10;

-- Sezonlara göre ev sahibi avantajı analizi
SELECT 
    Season,
    COUNT(*) as total_matches,
    SUM(CASE WHEN FullTimeResult = 'H' THEN 1 ELSE 0 END) as home_wins,
    SUM(CASE WHEN FullTimeResult = 'D' THEN 1 ELSE 0 END) as draws,
    SUM(CASE WHEN FullTimeResult = 'A' THEN 1 ELSE 0 END) as away_wins,
    ROUND(SUM(CASE WHEN FullTimeResult = 'H' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as home_win_percentage
FROM matches
GROUP BY Season
ORDER BY Season;

-- Detaylı Sezonlar Arası Gol Analizi
SELECT 
    Season,
    COUNT(*) as total_matches,
    SUM(FullTimeHomeGoals + FullTimeAwayGoals) as total_goals,
    ROUND(AVG(FullTimeHomeGoals + FullTimeAwayGoals), 2) as avg_goals_per_match,
    ROUND(AVG(FullTimeHomeGoals), 2) as avg_home_goals,
    ROUND(AVG(FullTimeAwayGoals), 2) as avg_away_goals,
    ROUND(AVG(HalfTimeHomeGoals + HalfTimeAwayGoals), 2) as avg_first_half_goals,
    ROUND(AVG((FullTimeHomeGoals + FullTimeAwayGoals) - (HalfTimeHomeGoals + HalfTimeAwayGoals)), 2) as avg_second_half_goals,
    ROUND(SUM(CASE WHEN (FullTimeHomeGoals + FullTimeAwayGoals) >= 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as high_scoring_match_percentage
FROM matches
GROUP BY Season
ORDER BY Season;

-- Sezonlara Göre Gol Dağılımı
SELECT 
    Season,
    SUM(CASE WHEN (FullTimeHomeGoals + FullTimeAwayGoals) = 0 THEN 1 ELSE 0 END) as zero_goals,
    SUM(CASE WHEN (FullTimeHomeGoals + FullTimeAwayGoals) = 1 THEN 1 ELSE 0 END) as one_goal,
    SUM(CASE WHEN (FullTimeHomeGoals + FullTimeAwayGoals) = 2 THEN 1 ELSE 0 END) as two_goals,
    SUM(CASE WHEN (FullTimeHomeGoals + FullTimeAwayGoals) = 3 THEN 1 ELSE 0 END) as three_goals,
    SUM(CASE WHEN (FullTimeHomeGoals + FullTimeAwayGoals) >= 4 THEN 1 ELSE 0 END) as four_or_more_goals
FROM matches
GROUP BY Season
ORDER BY Season; 