import datetime
import random
from game.shared.point import Point

class Director:
    """A person who directs the game.

    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
    """

    def __init__(self, keyboard_service, video_service):
        """Constructs a new Director using the specified keyboard and video services.

        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            video_service (VideoService): An instance of VideoService.
            _current_score : A variable to hold the current score.
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        self._current_score = int(0)

    def start_game(self, cast, cols, rows, cell_size, difficulty, Color):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.open_window()
        while self._video_service.is_window_open():
            self._get_inputs(cast)
            self._do_updates(cast, cols, rows, cell_size, difficulty, Color)
            self._do_outputs(cast)
        self._video_service.close_window()

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the robot.

        Args:
            cast (Cast): The cast of actors.
        """
        robot = cast.get_first_actor("robots")
        velocity = self._keyboard_service.get_direction()
        robot.set_velocity(velocity)

    def _do_updates(self, cast, cols, rows, cell_size, difficulty, Color):
        """Updates the robot's position, the artifact positions, and resolves any collisions with artifacts.
           Allows user to pick the level of difficulty in the program.
        
        Args:
            cast (Cast): The cast of actors.
            cols : The COLS specified in __main__
            cell_size: The CELL_SIZE specified in __main__
            difficulty: The difficulty selected in __main__ starting
        """
        #This IF/ELIF statement is used for difficulty settings to adjust speed of artifacts
        timeDelay = 1
        if difficulty == 2:
            timeDelay = .5
        elif difficulty == 3:
            timeDelay = .1

        x = random.randint(1, cols - 1)
        aPosition = Point(x, 0)
        aPosition = aPosition.scale(cell_size)

        banner = cast.get_first_actor("banners")
        robot = cast.get_first_actor("robots")
        artifacts = cast.get_actors("artifacts")
        currentTime = datetime.datetime.now()
        currentTimeStamp = currentTime.timestamp()

        banner.set_text(f"Score: {self._current_score}")
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        robot.move_next(max_x,max_y)
                
        for artifact in artifacts:
            x = random.randint(1, cols - 1)
            aPosition = Point(x, 0)
            aPosition = aPosition.scale(cell_size)
            if artifact.get_display() == 0:
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                color = Color(r, g, b)
                artifact.set_color(color)
                artifact.set_display(1)
                if artifact.get_text() == '*':
                    artifact.set_message(+1)
                else:
                    artifact.set_message(-1)
            if robot.get_position().equals(artifact.get_position()):
                message = artifact.get_message()
                self._current_score += message
                banner.set_text(f"Score: {self._current_score}")
                artifact.set_position(aPosition)
                # Works with timeDelay settings for difficulty settings
            if (currentTimeStamp - artifact.get_last_mod()) > timeDelay:
                aDirection = Point(0, cell_size)
                artifact.set_velocity(aDirection)
                artifact.move_next(max_x, max_y)
                artifact.set_last_mod()
                display = artifact.get_display()
                new_display = display + 1
                artifact.set_display(new_display)
                if artifact.get_position().get_y() == 0:
                    artifact.set_position(aPosition)
                    


    def _do_outputs(self, cast):
        """Draws the actors on the screen.

        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()
