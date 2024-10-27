from py_eureka_client import eureka_client


async def get_service_address_by_service_name(service, server):
    """Получение адреса микросервиса по его названию"""
    applications = await eureka_client.get_applications(server)
    instance = applications.get_application(service).instances[0]
    return instance.homePageUrl
