# _*_ coding:utf-8 _*_
import pytest
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import allure
from common.logger import logger

@pytest.fixture(autouse=True)
def print_template_jinrushengchandingdan(login):
    '''
    用例名称：验证打印模板节点进入正常
    左侧树搜索并点击进入生产订单节点验证
    '''
    driver = login
    driver.refresh()
    #等待左上角的全局标识并点击
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH, '//*[@fieldid="menu_img"]')))
    driver.find_element(By.XPATH, '//*[@fieldid="menu_img"]').click()
    #等待搜索标识的出现并点击
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@fieldid="nav-domain"]')))
    driver.find_element(By.XPATH, '//*[@fieldid="nav-domain"]').click()
    # 等待搜索框的出现并搜索打印模板后点击
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@class="search-input"]')))
    driver.find_element(By.XPATH, '//*[@class="search-input"]').send_keys("打印模板")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "searchTitle1")]/../ul/li[1]')))
    driver.find_element(By.XPATH, '//*[contains(@class, "searchTitle1")]/../ul/li[1]').click()

    #等待并检查进入打印模板节点成功
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@fieldid = "iprint-distribution-relations_btn"]')))
    element = driver.find_element(By.XPATH, '//*[@fieldid = "iprint-distribution-relations_btn"]')
    #元素文本验证
    assert element.text == "分配关系查询"

    #等待左侧树搜索框并录入生产订单节点名称
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@title="搜索模板分类"]')))
    driver.find_element(By.XPATH,'//*[@title="搜索模板分类"]').send_keys("生产订单")

    #等待菜单节点【生产订单】出现并点击进入
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@fieldid="iprint_classifytree_tree_title_productionorder.po_production_order"]')))
    driver.find_element(By.XPATH, '//*[@fieldid="iprint_classifytree_tree_title_productionorder.po_production_order"]').click()

    #等待新增按钮标识并验证
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@fieldid="iprint_add-iconfont"]')))
    #新增模板按钮标识存在验证
    element = driver.find_element(By.XPATH,'//*[@fieldid="iprint_add-iconfont"]')
    #元素存在性验证
    assert element is not None

@allure.epic("UI自动化")
@allure.feature("打印模板")
@allure.story("模板状态检查")
def test_template_status(login):
    '''
    这条用例用于检查打印模板的复制-启停-默认设置-删除
    '''
    driver = login
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@class="card_name"][text()="生产订单"]')))
    #用例前置：检查当前预用模板是否存在，存在就删掉
    with allure.step("用例前置：检查并删除当前用例涉及的打印模板"):
        try:
            element = driver.find_element(By.XPATH, '//*[text()="复制_状态验证"]')
            if element is not None:
                more = driver.find_element(By.XPATH, '//*[text()="复制_状态验证"]/../..//*[@fieldid="iprint_more-btn"]')
                ActionChains(driver).move_to_element(more).perform()
                time.sleep(5)
                driver.find_element(By.XPATH, '//*[@fieldid="iprint_delete-btn"][text()="删除"]').click()
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@fieldid="iprint_app_model_modal_title"]')))
                driver.find_element(By.XPATH, '//*[@fieldid="iprint_app_model_modal_footer_ok"]').click()
                WebDriverWait(driver, 20).until(
                    EC.invisibility_of_element_located((By.XPATH, '//*[text()="复制_状态验证"]')))
        except NoSuchElementException:
            pass
    #等待并复制系统模板并验证目标模板存在
    #等待系统级模板并点击复制按钮
    with allure.step("开始复制系统模板进行新模板的创建"):
        logger.info("开始复制系统模板")
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'//*[@class="card_name"][text()="生产订单"]')))
        driver.find_element(By.XPATH,'//*[text()="生产订单"]/..//*[@fieldid="iprint_copy-btn"]').click()
        #获取当前窗口句柄
        print_handle = driver.current_window_handle
        #修改复制模板名称并确定
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'//*[@fieldid="print_multilang_requireNoAutoComplete"]')))
        #清空原内容
        #clear方法使用无效，改为模拟键盘删除方法
        #driver.find_element(By.XPATH, '//*[@fieldid="print_multilang_requireNoAutoComplete"]').clear()
        element = driver.find_element(By.XPATH, '//*[@fieldid="print_multilang_requireNoAutoComplete"]')
        #模拟control+a键盘全选
        element.send_keys(Keys.CONTROL + 'a')
        #模拟键盘的删除delete
        element.send_keys(Keys.DELETE)
        #写入新内容
        driver.find_element(By.XPATH,'//*[@fieldid="print_multilang_requireNoAutoComplete"]').send_keys("复制_状态验证")
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'//*[@fieldid="iprint_CopyTemp_model_modal_footer_ok"]')))
        driver.find_element(By.XPATH,'//*[@fieldid="iprint_CopyTemp_model_modal_footer_ok"]').click()
        #返回打印模板浏览器页面
        WebDriverWait(driver,20).until(lambda a:len(a.window_handles)>1)
        for handle in driver.window_handles:
            if handle !=print_handle:
                driver.switch_to.window(handle)
                driver.close()
                driver.switch_to.window(print_handle)
                break
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'//*[text()="复制_状态验证"]')))
        element = driver.find_element(By.XPATH,'//*[text()="复制_状态验证"]')
        assert element.text == "复制_状态验证"
        logger.info("新增复制模板验证通过")
    with allure.step("验证新增模板为已启用状态"):
        logger.info("验证新增模板为已启用状态")
        element = driver.find_element(By.XPATH,'//*[text()="复制_状态验证"]/../..//*[text()="已启用"]')
        assert element is not None
    with allure.step("模板启停验证"):
        logger.info("模板启停验证")
        more = driver.find_element(By.XPATH,'//*[text()="复制_状态验证"]/../..//*[@fieldid="iprint_more-btn"]')
        ActionChains(driver).move_to_element(more).perform()
    with allure.step("点击停用按钮"):
        logger.info("点击停用按钮")
        driver.find_element(By.XPATH,'//*[@fieldid="iprint_disuse-btn"]').click()
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'//*[text()="复制_状态验证"]/../..//*[text()="已停用"]')))
        element = driver.find_element(By.XPATH,'//*[text()="复制_状态验证"]/../..//*[text()="已停用"]')
        assert element is not None
    with allure.step("点击启动按钮"):
        logger.info("点击启动按钮")
        ActionChains(driver).move_to_element(more).perform()
        driver.find_element(By.XPATH, '//*[@fieldid="iprint_use-btn"]').click()
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[text()="复制_状态验证"]/../..//*[text()="已启用"]')))
        element = driver.find_element(By.XPATH, '//*[text()="复制_状态验证"]/../..//*[text()="已启用"]')
        assert element is not None
    logger.info("打印模板的启停状态切换验证通过")
    with allure.step("模板默认标签验证"):
        logger.info("模板默认标签验证")
        logger.info("设置默认")
        ActionChains(driver).move_to_element(more).perform()
        driver.find_element(By.XPATH, '//*[@fieldid="iprint_default-btn"]').click()
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[text()="复制_状态验证"]/../..//*[text()="默认"]')))
        element = driver.find_elements(By.XPATH, '//*[text()="复制_状态验证"]/../..//*[text()="默认"]')
        assert element is not None
        logger.info("取消默认设置")
        time.sleep(3)
        ActionChains(driver).move_to_element(more).perform()
        driver.find_element(By.XPATH, '//*[@fieldid="iprint_cancel_default-btn"]').click()
        WebDriverWait(driver, 20).until_not(EC.presence_of_element_located((By.XPATH, '//*[text()="复制_状态验证"]/../..//*[text()="默认"]')))
        element = driver.find_elements(By.XPATH, '//*[text()="复制_状态验证"]/../..//*[text()="默认"]')
        assert len(element) == 0
        logger.info("打印模板的默认标签配置取消验证通过")
    with allure.step("执行打印模板的删除操作"):
        ActionChains(driver).move_to_element(more).perform()
        driver.find_element(By.XPATH, '//*[@fieldid="iprint_delete-btn"][text()="删除"]').click()
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@fieldid="iprint_app_model_modal_title"]')))
        driver.find_element(By.XPATH, '//*[@fieldid="iprint_app_model_modal_footer_ok"]').click()
        WebDriverWait(driver, 20).until_not(EC.presence_of_element_located((By.XPATH, '//*[text()="复制_状态验证"]')))
        tem_element = driver.find_elements(By.XPATH, '//*[text()="复制_状态验证"]')
        assert len(tem_element) == 0
        logger.info("新增打印模板删除完成")

@allure.epic("UI自动化")
@allure.feature("打印模板")
@allure.story("模板属性默认值检查")
def test_design_properties_default_value(login):
    logger.info("这条用例仅作打印模板模板属性默认值检查")
    driver = login
    with allure.step("用例前置：检查当前预用模板是否存在，存在就删掉"):
        logger.info("用例前置：检查当前预用模板是否存在，存在就删掉")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="card_name"][text()="生产订单"]')))
        try:
            element = driver.find_element(By.XPATH, '//*[text()="复制_模板属性验证"]')
            if element is not None:
                more = driver.find_element(By.XPATH, '//*[text()="复制_模板属性验证"]/../..//*[@fieldid="iprint_more-btn"]')
                ActionChains(driver).move_to_element(more).perform()
                time.sleep(5)
                driver.find_element(By.XPATH, '//*[@fieldid="iprint_delete-btn"][text()="删除"]').click()
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@fieldid="iprint_app_model_modal_title"]')))
                driver.find_element(By.XPATH, '//*[@fieldid="iprint_app_model_modal_footer_ok"]').click()
                WebDriverWait(driver, 20).until(
                    EC.invisibility_of_element_located((By.XPATH, '//*[text()="复制_模板属性验证"]')))
        except NoSuchElementException:
            pass
    with allure.step("复制系统模板并获取当前页面句柄"):
        logger.info("复制系统模板")
        driver.find_element(By.XPATH, '//*[text()="生产订单"]/..//*[@fieldid="iprint_copy-btn"]').click()
        # 获取当前窗口句柄
        printlist_handle = driver.current_window_handle
    with allure.step("修改复制模板名称并确定"):
        logger.info("修改复制模板名称并确定")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@fieldid="print_multilang_requireNoAutoComplete"]')))
        # 清空原内容
        # clear方法使用无效，改为模拟键盘删除方法
        # driver.find_element(By.XPATH, '//*[@fieldid="print_multilang_requireNoAutoComplete"]').clear()
        element = driver.find_element(By.XPATH, '//*[@fieldid="print_multilang_requireNoAutoComplete"]')
        # 模拟control+a键盘全选
        element.send_keys(Keys.CONTROL + 'a')
        # 模拟键盘的删除delete
        element.send_keys(Keys.DELETE)
        # 写入新内容
        driver.find_element(By.XPATH, '//*[@fieldid="print_multilang_requireNoAutoComplete"]').send_keys("复制_模板属性验证")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@fieldid="iprint_CopyTemp_model_modal_footer_ok"]')))
        driver.find_element(By.XPATH, '//*[@fieldid="iprint_CopyTemp_model_modal_footer_ok"]').click()
    with allure.step("进入打印模板设计器浏览器页面"):
        logger.info("进入打印模板设计器浏览器页面")
        WebDriverWait(driver, 20).until(lambda a: len(a.window_handles) > 1)
        for handle in driver.window_handles:
            if handle != printlist_handle:
                driver.switch_to.window(handle)
        WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="set-propty"]')))
        driver.find_element(By.XPATH,'//*[@id="set-propty"]').click()
    with allure.step("验证模板编码框不可编辑"):
        logger.info("验证模板编码框不可编辑")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@fieldid="design|InputText|tenantPageCode|Input"]')))
        element = driver.find_element(By.XPATH,'//*[@fieldid="design|InputText|tenantPageCode|Input"]')
        assert not element.is_enabled()
    with allure.step("验证模板名称与新增该模板配置的名称一致"):
        logger.info("验证模板名称与新增该模板配置的名称一致")
        time.sleep(3)
        element = driver.find_element(By.XPATH,'//*[@fieldid="design|InputText|uititle|Input"]')
        assert element.get_attribute("value") == "复制_模板属性验证"
    with allure.step("验证横向矩阵默认值为1"):
        logger.info("验证横向矩阵默认值为1")
        time.sleep(3)
        element = driver.find_element(By.XPATH,'//*[@fieldid="design|InputNumber|MergePrintPagesX|InputNumber"]')
        assert element.get_attribute("value") == "1"
    with allure.step("验证总想矩阵默认值为1"):
        logger.info("验证总想矩阵默认值为1")
        time.sleep(3)
        element = driver.find_element(By.XPATH, '//*[@fieldid="design|InputNumber|MergePrintPagesY|InputNumber"]')
        assert element.get_attribute("value") == "1"
    with allure.step("验证循环主体为【暂无】"):
        logger.info("验证循环主体为【暂无】")
        time.sleep(3)
        element = driver.find_element(By.XPATH,'//*[@fieldid="design|InputSelect|mainTable|Select_search_input"]')
        assert element.get_attribute("value") == "暂无"
    with allure.step("验证多页面打印方式默认值为【按单据】"):
        logger.info("验证多页面打印方式默认值为【按单据】")
        time.sleep(3)
        element = driver.find_element(By.XPATH, '//*[@fieldid="design|InputSelect|pageTemplateCircle|Select_search_input"]')
        assert element.get_attribute("value") == "按模板页面"
    #下边这几个验证项是检查属性按钮开关状态的
    with allure.step("单据间隔打印默认关闭验证"):
        logger.info("单据间隔打印默认关闭验证")
        time.sleep(3)
        element = driver.find_element(By.XPATH,'//*[@fieldid="design|InputBool|intervalPrinting|Switch"]')
        assert 'checked' not in element.get_attribute("class")
    with allure.step("双面打印默认关闭验证"):
        logger.info("双面打印默认关闭验证")
        time.sleep(3)
        element = driver.find_element(By.XPATH, '//*[@fieldid="design|InputBool|duplexPrinting|Switch"]')
        assert 'checked' not in element.get_attribute("class")
    with allure.step("仅打印有效审批意见默认关闭验证"):
        logger.info("仅打印有效审批意见默认关闭验证")
        time.sleep(3)
        element = driver.find_element(By.XPATH, '//*[@fieldid="design|InputBool|noPrintReverse|Switch"]')
        assert 'checked' not in element.get_attribute("class")
    with allure.step("不打印无效抢占审批默认关闭验证"):
        logger.info("不打印无效抢占审批默认关闭验证")
        time.sleep(3)
        element = driver.find_element(By.XPATH, '//*[@fieldid="design|InputBool|excludeGrab|Switch"]')
        assert 'checked' not in element.get_attribute("class")
    with allure.step("不打印自动跳过审批默认关闭验证"):
        logger.info("不打印自动跳过审批默认关闭验证")
        time.sleep(3)
        element = driver.find_element(By.XPATH, '//*[@fieldid="design|InputBool|excludeNoUserCompleteAuto|Switch"]')
        assert 'checked' not in element.get_attribute("class")
        logger.info("打印模板设计器模板属性默认值验证通过")
    with allure.step("关闭当前句柄页面并删除本次新增打印模板"):
        driver.close()
        driver.switch_to.window(printlist_handle)
        more = driver.find_element(By.XPATH, '//*[text()="复制_模板属性验证"]/../..//*[@fieldid="iprint_more-btn"]')
        logger.info("执行打印模板的删除操作")
        ActionChains(driver).move_to_element(more).perform()
        driver.find_element(By.XPATH, '//*[@fieldid="iprint_delete-btn"][text()="删除"]').click()
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@fieldid="iprint_app_model_modal_title"]')))
        driver.find_element(By.XPATH, '//*[@fieldid="iprint_app_model_modal_footer_ok"]').click()
        WebDriverWait(driver, 20).until_not(EC.presence_of_element_located((By.XPATH, '//*[text()="复制_模板属性验证"]')))
        tem_element = driver.find_elements(By.XPATH, '//*[text()="复制_模板属性验证"]')
        assert len(tem_element) == 0
        logger.info("新增打印模板删除完成")
@allure.epic("UI自动化")
@allure.feature("打印模板")
@allure.story("设计器列表新增检查")
def test_kongjian_list_drag_default_value(login):
    logger.info("该用例用于进行打印模板设计器中列表控件的删除、新增、配置后的默认属性验证")
    driver = login
    logger.info("用例前置：检查当前预用模板是否存在，存在就删掉")
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@class="card_name"][text()="生产订单"]')))
    with allure.step("检查并删除历史执行中遗留的本次用例使用模板名称模板"):
        try:
            element = driver.find_element(By.XPATH, '//*[text()="复制_列表属性验证"]')
            if element is not None:
                more = driver.find_element(By.XPATH, '//*[text()="复制_列表属性验证"]/../..//*[@fieldid="iprint_more-btn"]')
                ActionChains(driver).move_to_element(more).perform()
                time.sleep(5)
                driver.find_element(By.XPATH, '//*[@fieldid="iprint_delete-btn"][text()="删除"]').click()
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@fieldid="iprint_app_model_modal_title"]')))
                driver.find_element(By.XPATH, '//*[@fieldid="iprint_app_model_modal_footer_ok"]').click()
                WebDriverWait(driver, 20).until(
                    EC.invisibility_of_element_located((By.XPATH, '//*[text()="复制_列表属性验证"]')))
        except NoSuchElementException:
            pass

    with allure.step("获取当前句柄"):
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="card_name"][text()="生产订单"]')))
        driver.find_element(By.XPATH, '//*[text()="生产订单"]/..//*[@fieldid="iprint_copy-btn"]').click()
        # 获取当前窗口句柄
        printlist_handle = driver.current_window_handle
    with allure.step("进行目标模板的创建"):
        logger.info("修改复制模板名称并确定")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@fieldid="print_multilang_requireNoAutoComplete"]')))
        # 清空原内容
        # clear方法使用无效，改为模拟键盘删除方法
        # driver.find_element(By.XPATH, '//*[@fieldid="print_multilang_requireNoAutoComplete"]').clear()
        element = driver.find_element(By.XPATH, '//*[@fieldid="print_multilang_requireNoAutoComplete"]')
        # 模拟control+a键盘全选
        element.send_keys(Keys.CONTROL + 'a')
        # 模拟键盘的删除delete
        element.send_keys(Keys.DELETE)
        # 写入新内容
        driver.find_element(By.XPATH, '//*[@fieldid="print_multilang_requireNoAutoComplete"]').send_keys(
            "复制_列表属性验证")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@fieldid="iprint_CopyTemp_model_modal_footer_ok"]')))
        driver.find_element(By.XPATH, '//*[@fieldid="iprint_CopyTemp_model_modal_footer_ok"]').click()
    with allure.step("进入打印模板设计器浏览器页面"):
        logger.info("进入打印模板设计器浏览器页面")
        WebDriverWait(driver, 20).until(lambda a: len(a.window_handles) > 1)
        for handle in driver.window_handles:
            if handle != printlist_handle:
                driver.switch_to.window(handle)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="set-propty"]')))
    #开始进行列表控件的新增、验证过程
    with allure.step("等待并删除画布上已经配置好的列表控件"):
        logger.info("等待并删除画布上已经配置好的列表控件")
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'//*[@title="列表: 生产订单表体"]')))
        element = driver.find_element(By.XPATH,'//*[@title="列表: 生产订单表体"]')
        if element:
            element.click()
            #等待删除按钮出现并点击
            WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'//*[@title="列表: 生产订单表体"]/..//*[contains(@class,"delete-button")]')))
            driver.find_element(By.XPATH,'//*[@title="列表: 生产订单表体"]/..//*[contains(@class,"delete-button")]').click()
            element = driver.find_elements(By.XPATH, '//*[@title="列表: 生产订单表体"]')
            assert len(element) ==0
            logger.info("系统预置的列表在画布删除成功")
    #通过拖拽添加新列表控件并进行元素配置
    with allure.step("通过拖拽添加新列表控件"):
        #配置列表控件element
        list_element = driver.find_element(By.XPATH,'//*[@fieldid="design|ComponentGroup|Panel|tableGroup|table"]')
        logger.info("获取到列表控件")
        #配置画布目标element
        targ_element = driver.find_element(By.XPATH,'//*[@id="watermarkWordCover"]')
        logger.info("获取到画布")
        #将列表控件移动到目标位置
        #ActionChains(driver).drag_and_drop(list_element,targ_element).perform()
        action = ActionChains(driver)
        action.move_to_element(list_element).perform()
        action.click_and_hold()
        # 3. 将鼠标移动到画布的中心位置
        # 计算画布中心坐标
        logger.info("x坐标是"+str(targ_element.location['x']))
        logger.info("y坐标是"+str(targ_element.location['y']))
        canvas_center_x = targ_element.location['x'] + 200
        canvas_center_y = targ_element.location['y'] + 200
        action.move_by_offset(canvas_center_x - list_element.location['x'],
                               canvas_center_y - list_element.location['y']).perform()
        action.release().perform()
        logger.info("列表控件完成向画布拖入操作")
        logger.info("验证列表设置弹窗弹出正常")
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'//*[@id="inputDesignModalHeader"]')))
        list_settings_element = driver.find_element(By.XPATH,'//*[@id="inputDesignModalHeader"]')
        time.sleep(10)
        assert list_settings_element is not None
    with allure.step("开始配置列表的三个指定字段"):
        logger.info("开始配置列表的三个指定字段")
        #搜索选择字段
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'//*[@placeholder="请输入查找内容"]')))
        element = driver.find_element(By.XPATH,'//*[@placeholder="请输入查找内容"]')
        logger.info("搜索并选择字段【开工日期】")
        element.send_keys("开工日期")
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'//*[@id="Order.orderProduct.startDate"]')))
        driver.find_element(By.XPATH,'//*[@id="Order.orderProduct.startDate"]').click()
        #删除搜索框内容
        element = driver.find_element(By.XPATH, '//*[@value="开工日期"][@type="search"]')
        # 模拟control+a键盘全选
        element.click()
        element.send_keys(Keys.CONTROL + 'a')
        # 模拟键盘的删除delete
        element.send_keys(Keys.DELETE)
        time.sleep(3)
        logger.info("开始验证第一个字段选择是否正常")
        yuansu1 = driver.find_element(By.XPATH,'//*[@title="Order.orderProduct.startDate"]')
        assert yuansu1 is not None
        logger.info("搜索并选择字段【完工日期】")
        element.send_keys("完工日期")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="Order.orderProduct.finishDate"]')))
        driver.find_element(By.XPATH, '//*[@id="Order.orderProduct.finishDate"]').click()
        # 删除搜索框内容
        element = driver.find_element(By.XPATH, '//*[@value="完工日期"][@type="search"]')
        # 模拟control+a键盘全选
        element.send_keys(Keys.CONTROL + 'a')
        # 模拟键盘的删除delete
        element.send_keys(Keys.DELETE)
        time.sleep(3)
        logger.info("开始验证第二个字段选择是否正常")
        yuansu2 = driver.find_element(By.XPATH, '//*[@title="Order.orderProduct.finishDate"]')
        assert yuansu2 is not None
        logger.info("搜索并选择字段【生产数量】")
        element.send_keys("生产数量")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="Order.orderProduct.quantity"]')))
        driver.find_element(By.XPATH, '//*[@id="Order.orderProduct.quantity"]').click()
        # 删除搜索框内容
        element = driver.find_element(By.XPATH, '//*[@value="生产数量"][@type="search"]')
        # 模拟control+a键盘全选
        element.send_keys(Keys.CONTROL + 'a')
        # 模拟键盘的删除delete
        element.send_keys(Keys.DELETE)
        time.sleep(3)
        logger.info("开始验证第三个字段选择是否正常")
        yuansu3 = driver.find_element(By.XPATH, '//*[@title="Order.orderProduct.quantity"]')
        assert yuansu3 is not None
    with allure.step("点击确定保存列表"):
        logger.info("点击确定保存列表")
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'//*[text()="确定"]')))
        driver.find_element(By.XPATH,'//*[text()="确定"]').click()
    time.sleep(3)
    with allure.step("开始验证新增列表是否展示正常"):
        logger.info("开始验证新增列表是否展示正常")
        elements = driver.find_elements(By.XPATH, '//*[@id="inputDesignModalHeader"]')
        assert len(elements) == 0, "列表设置弹窗未关闭"
        #检查列表配置后在画布上展示正常
        new_list_title = driver.find_element(By.XPATH,'//*[@id="watermarkWordCover"]//*[@title="列表: 生产订单产品"]')
        assert new_list_title is not None
    with allure.step("验证列表默认没有开启承前过次页，且开启设置正常"):
        logger.info("验证列表默认没有开启承前过次页，且开启设置正常")
        chengqianye = driver.find_elements(By.XPATH,'//*[text()="承前页"]')
        guociye = driver.find_elements(By.XPATH,'//*[text()="过次页"]')
        assert len(chengqianye) == 0,"元素'承前页'存在，预期不存在"
        assert len(guociye) == 0,"元素'过次页'存在，预期不存在"
    with allure.step("开启承前过次开关"):
        logger.info("开启承前过次开关")
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'//*[@fieldid="design|InputBool|pastAcceptance|Switch"]')))
        driver.find_element(By.XPATH,'//*[@fieldid="design|InputBool|pastAcceptance|Switch"]').click()
    time.sleep(3)
    with allure.step("验证开启后承前页、过次页两行出现"):
        logger.info("验证开启后承前页、过次页两行出现")
        assert len(chengqianye) != 0, "元素'承前页'存在，预期存在"
        assert len(guociye) == 0, "元素'过次页'存在，预期存在"

    with allure.step("用例后置：删除本用例新增模板"):
        logger.info("用例后置：删除本用例新增模板")
        driver.switch_to.window(printlist_handle)
        try:
            element = driver.find_element(By.XPATH, '//*[text()="复制_列表属性验证"]')
            if element is not None:
                more = driver.find_element(By.XPATH, '//*[text()="复制_列表属性验证"]/../..//*[@fieldid="iprint_more-btn"]')
                ActionChains(driver).move_to_element(more).perform()
                time.sleep(5)
                driver.find_element(By.XPATH, '//*[@fieldid="iprint_delete-btn"][text()="删除"]').click()
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@fieldid="iprint_app_model_modal_title"]')))
                driver.find_element(By.XPATH, '//*[@fieldid="iprint_app_model_modal_footer_ok"]').click()
                logger.info("本次用例新增模板删除完成，用例执行成功")
        except NoSuchElementException:
            pass