from game.casting.actor import Actor
import datetime


class Artifact(Actor):
    """
    An item of cultural or historical interest. 
    
    The responsibility of an Artifact is to provide a message about itself.

    Attributes:
        _message (string): A short description about the artifact.
        _last_mod (float): Holds a timestamp for the last modification of velocity for the artificats. 
                           This is used to control artifact scroll speed.
    """
    def __init__(self):
        """
        Adds _message details for scoring and _last_mod for artifact movement speed.
        """
        super().__init__()
        self._message = ""
        self._last_mod = float(0)
                
    def get_message(self):
        """Gets the artifact's message.
        
        Returns:
            string: The message.
        """
        return self._message
    
    def set_message(self, message):
        """Updates the message to the given one.
        
        Args:
            message (string): The given message.
        """
        self._message = message

    def get_last_mod(self):
        """Gets the artifact's last modifacation time stamp.
        
        Returns:
            float: The last modifacation time stamp.
        """
        return self._last_mod

    def set_last_mod(self):
        """Updates the last modifaction attribute.
        
        Args:
            last_mod (float): The given timestamp
        """
        current_time = datetime.datetime.now()
        timestamp =current_time.timestamp()
        self._last_mod = timestamp
    
    
 
        

        
