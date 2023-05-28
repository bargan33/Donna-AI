from donna_session import DonnaSession
from donna_ranking import DonnaRanking

ds = DonnaSession('serde/Test1')
dr = DonnaRanking()
dr.init(ds)
dr.evaluate()
