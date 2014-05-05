#!/usr/bin/python

import os, sys
import logging as log

class WebService(object):
    @staticmethod
    def load_handlers(root_dir):
        sys.path.insert(0, root_dir)
        handlers_path = os.path.sep.join([root_dir, 'handlers'])
        if not os.path.isdir(handlers_path):
            log.critical("WebService handlers directory does not exist: %s" % (
                handlers_path,
            ))
            sys.exit(1)
        handler_urls = []
        handler_failure = False
        handler_error = None
        service_list = os.listdir(handlers_path)
        service_list.sort()
        for service_filename in service_list:
            if service_filename[-3:] != '.py':
                    continue
            service = service_filename[:-3]
            if service == '__init__':
                    continue
            handler_module_path = '.'.join([
                    'handlers', service,
            ])
            try:
                handler_module = __import__(
                    handler_module_path, {}, {}, [service],
                )
            except ImportError, e:
                handler_failure = True
                log.critical('Unable to import "%s": %s' % (
                    service, str(e),
                ))
                if handler_error is None:
                    handler_error = 'ImportError'
                continue
            except SyntaxError, e:
                handler_failure = True
                log.critical('Syntax error in "%s": %s' % (
                    service, str(e),
                ))
                if handler_error is None:
                    handler_error = 'SyntaxError'
                continue
            try:
                handler = getattr(handler_module, service)
            except AttributeError, e:
                handler_failure = True
                log.critical('Invalid class in "%s": %s' % (
                    service, str(e),
                ))
                if handler_error is None:
                    handler_error = 'AttributeError'
                continue
            WebService.add_handler(handler.url(), handler, handler_urls)
            if handler.url()[:-1] != '/':
                WebService.add_handler(handler.url() + '/', handler, handler_urls)
        if handler_failure:
            log.critical('loading handlers failed: %s' % (
                handler_error,
            ))
            sys.exit(1)
        del sys.path[0]
        return handler_urls

    @staticmethod
    def add_handler(handler_url, handler, handler_urls_list):
        log.info('Loading Handler URL: %s' % handler_url)
        handler_urls_list.append((handler_url, handler)) 
