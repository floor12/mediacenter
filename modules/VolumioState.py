
class VolumioState():
  currentState = {'status':'stop'}

  def isPlaying(self):
    if (self.currentState['status'] == 'play'):
      return True
    else:
       return False