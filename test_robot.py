import pytest

from robot import Robot, Direction, IllegalMoveException


@pytest.fixture
def robot():
    return Robot()


def test_constructor(robot):
    state = robot.state()

    assert state['direction'] == Direction.NORTH
    assert state['row'] == 10
    assert state['col'] == 1


def test_east_turn(robot):
    robot.turn()

    state = robot.state()
    assert state['direction'] == Direction.EAST


def test_south_turn(robot):
    robot.turn()
    robot.turn()

    state = robot.state()
    assert state['direction'] == Direction.SOUTH


def test_west_turn(robot):
    robot.turn()
    robot.turn()
    robot.turn()

    state = robot.state()
    assert state['direction'] == Direction.WEST


def test_north_turn(robot):
    robot.turn()
    robot.turn()
    robot.turn()
    robot.turn()

    state = robot.state()
    assert state['direction'] == Direction.NORTH


def test_illegal_move1(robot):
    robot.turn();
    robot.turn();

    with pytest.raises(IllegalMoveException):
        robot.move()

def test_illegal_move2(robot):
    robot.turn()
    robot.turn()
    robot.turn()  ## SOUTH
    with pytest.raises(IllegalMoveException):
        robot.move()


def test_illegal_move3(robot):
    robot._state.row = 1  ## NORTH row: 1 col: 1
    with pytest.raises(IllegalMoveException):
        robot.move()


def test_illegal_move4(robot):
    robot._state.col = 10
    robot.turn()  ## EAST row: 10 col: 10
    with pytest.raises(IllegalMoveException):
        robot.move()


def test_move_north(robot):
    robot.move()
    state = robot.state()
    assert state['row'] == 9
    assert state['col'] == 1


def test_move_east(robot):
    robot.turn()  ## EAST
    robot.move()
    state = robot.state()
    assert state['row'] == 10
    assert state['col'] == 2


def test_move_south(robot):
    robot.move()  ## row: 9 col: 1
    robot.turn()
    robot.turn()  ## SOUTH
    robot.move()
    state = robot.state()
    assert state['row'] == 10
    assert state['col'] == 1


def test_move_west(robot):
    robot.turn() ## EAST
    robot.move() ## row: 10 col: 2
    robot.turn()
    robot.turn() ## WEST
    robot.move()
    state = robot.state()
    assert state['row'] == 10
    assert state['col'] == 1


def test_back_track_without_history(robot):
    robot.back_track()
    state = robot.state()
    assert state['direction'] == Direction.NORTH
    assert state['row'] == 10
    assert state['col'] == 1


def test_back_track_after_move(robot):
    robot.move()
    robot.back_track()
    state = robot.state()
    assert state['direction'] == Direction.NORTH
    assert state['row'] == 10
    assert state['col'] == 1


def test_back_track_after_turn(robot):
    robot.turn()
    robot.back_track()
    state = robot.state()
    assert state['direction'] == Direction.NORTH
    assert state['row'] == 10
    assert state['col'] == 1


def test_back_track_after_multiple_moves(robot):
    robot.move()  ## row: 9 col: 1
    robot.move()  ## row: 8 col: 1
    robot.move()  ## row: 7 col: 1
    robot.back_track()
    state = robot.state()
    assert state['direction'] == Direction.NORTH
    assert state['row'] == 8
    assert state['col'] == 1


def test_back_track_after_multiple_moves_all(robot):
    robot.move()  ## row: 9 col: 1
    robot.move()  ## row: 8 col: 1
    robot.move()  ## row: 7 col: 1
    robot.back_track()
    robot.back_track()
    robot.back_track()
    state = robot.state()
    assert state['direction'] == Direction.NORTH
    assert state['row'] == 10
    assert state['col'] == 1