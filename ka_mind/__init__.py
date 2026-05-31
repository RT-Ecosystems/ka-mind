# KA-Mind Library — NeuraBrain Technique
# Lazy imports to prevent circular dependency
__version__   = '2.1.0'
__technique__ = 'NeuraBrain'

def get_model(name='KA-Mind', domain='General'):
    from .framework.model import KaModel
    return KaModel(name, domain)
