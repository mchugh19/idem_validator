def traverse_dict_and_list(hub, data, key, default=None, delimiter=":"):
    """
    Traverse a dict or list using a colon-delimited (or otherwise delimited,
    using the 'delimiter' param) target string. The target 'foo:bar:0' will
    return data['foo']['bar'][0] if this value exists, and will otherwise
    return the dict in the default argument.
    Function will automatically determine the target type.
    The target 'foo:bar:0' will return data['foo']['bar'][0] if data like
    {'foo':{'bar':['baz']}} , if data like {'foo':{'bar':{'0':'baz'}}}
    then return data['foo']['bar']['0']
    """
    ptr = data
    for each in key.split(delimiter):
        if isinstance(ptr, list):
            try:
                idx = int(each)
            except ValueError:
                embed_match = False
                # Index was not numeric, lets look at any embedded dicts
                for embedded in (x for x in ptr if isinstance(x, dict)):
                    try:
                        ptr = embedded[each]
                        embed_match = True
                        break
                    except KeyError:
                        pass
                if not embed_match:
                    # No embedded dicts matched, return the default
                    return default
            else:
                try:
                    ptr = ptr[idx]
                except IndexError:
                    return default
        else:
            try:
                ptr = ptr[each]
            except KeyError:
                import yaml

                # YAML-load the current key (catches integer/float dict keys)
                try:
                    loaded_key = yaml.safe_load(each)
                except Exception:  # pylint: disable=broad-except
                    return default
                if loaded_key == each:
                    # After YAML-loading, the desired key is unchanged. This
                    # means that the KeyError caught above is a legitimate
                    # failure to match the desired key. Therefore, return the
                    # default.
                    return default
                else:
                    # YAML-loading the key changed its value, so re-check with
                    # the loaded key. This is how we can match a numeric key
                    # with a string-based expression.
                    try:
                        ptr = ptr[loaded_key]
                    except (KeyError, TypeError):
                        return default
            except TypeError:
                return default
    return ptr
