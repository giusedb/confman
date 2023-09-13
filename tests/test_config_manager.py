import json
import os
import pytest

from pyconfman.manager import Config
CONF_DIR = None


@pytest.fixture
def config(tmp_path):
    global CONF_DIR
    if not CONF_DIR:
        CONF_DIR = tmp_path
    return Config(CONF_DIR)


def test_default_dir():
    conf = Config()
    assert conf._dir == f'{os.environ["HOME"]}/.config/confman'


def test_creation(config: Config):
    my_dict = {'name': 'John', 'last_name': 'Doe'}
    config['test_user'] = my_dict
    file_name = os.path.join(config._dir, 'test_user.json')
    assert os.path.exists(config._dir)
    assert os.path.exists(file_name)
    with open(file_name) as f:
        content = json.load(f)
        assert content == my_dict


def test_path(config: Config):
    n, c, k, p, _ = config._split_path('foo.test.foo.bar.a')
    assert ','.join(p) == 'foo,test,foo,bar,a'
    config.load('foo.test.foo.bar', {'a': 1, 'b': 2})
    assert n == {}
    assert c == config


def test_load(config: Config, tmp_path_factory):
    config.load('test.foo.bar', {'a': 1, 'b': 2})
    assert config['test']['foo']['bar']['a'] == 1
    assert config.get('test.foo.bar.b') == 2
    assert type(config.get('test.foo.bar')) == dict
    bar_dir = tmp_path_factory.mktemp('bar')
    json_input = os.path.join(bar_dir, 'x.json')
    with open(json_input, 'w') as f:
        json.dump({'foo': 'bar'}, f)
    config.load('test.test.far.west', json_input)
    assert config.get('test.test.far.west.foo') == 'bar'
    assert type(config.get('test')) == Config
    config.load('bar', {'x': 2})
    assert config.get('bar') == {'x': 2}
    assert config['bar']['x'] == 2


def test_set_key(config: Config):
    config['xyz'] = 29
    assert config['xyz'] == 29
    with open(os.path.join(config._dir, 'xyz.json')) as f:
        content = json.load(f)
        assert content == 29


def test_set_key_on_existing_dict(config: Config):
    config.load('a.b', {'c': 2})
    config.set_key('a.b.c', 1)
    assert config.get('a.b.c') == 1


def test_set_key_on_sub_dict(config: Config):
    config.load('a.b', {'c': {'d': 2, 'e': 3}})
    config.set_key('a.b.c.d', 1)
    assert config.get('a.b.c') == {'d': 1, 'e': 3}


def test_set_key_creates_dict(config: Config):
    config.load('non.existing.object', {})
    config.set_key('non.existing.object.with.dict.a', 1)
    config.set_key('non.existing.object.with.dict.b', 2)
    assert config.get('non.existing.object.with.dict') == {'a': 1, 'b': 2}


def test_set_key_non_existing(config: Config):
    with pytest.raises(KeyError):
        config.set_key('nonetheless.it.may.work', 100)
    with pytest.raises(KeyError):
        config.get('nonetheless.it.may.work')
