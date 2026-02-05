# _*_ coding:utf-8 _*_
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

def test_print_template_search(login):
    '''
    用例名称：验证打印模板节点进入正常
    该用例需要与test_tenant_id_check串行，否则后续需要优化到该租户下执行
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

def test_search_lingyujieidan(login):
    '''
    用例名称：左侧树搜索并点击进入生产订单节点验证
    该用例建议与test_print_template_search串行
    '''
    driver = login
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

def test_template_status(login):
    '''
    这条用例用于检查打印模板的复制-启停-默认设置-删除
    '''
    driver = login
    #用例前置：检查当前预用模板是否存在，存在就删掉
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
    print("新增复制模板验证通过")
    #验证新增模板为已启用状态
    element = driver.find_element(By.XPATH,'//*[text()="复制_状态验证"]/../..//*[text()="已启用"]')
    assert element is not None
    #模板启停验证
    more = driver.find_element(By.XPATH,'//*[text()="复制_状态验证"]/../..//*[@fieldid="iprint_more-btn"]')
    ActionChains(driver).move_to_element(more).perform()
    #点击停用按钮
    driver.find_element(By.XPATH,'//*[@fieldid="iprint_disuse-btn"]').click()
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'//*[text()="复制_状态验证"]/../..//*[text()="已停用"]')))
    element = driver.find_element(By.XPATH,'//*[text()="复制_状态验证"]/../..//*[text()="已停用"]')
    assert element is not None
    #点击启动按钮
    ActionChains(driver).move_to_element(more).perform()
    driver.find_element(By.XPATH, '//*[@fieldid="iprint_use-btn"]').click()
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[text()="复制_状态验证"]/../..//*[text()="已启用"]')))
    element = driver.find_element(By.XPATH, '//*[text()="复制_状态验证"]/../..//*[text()="已启用"]')
    assert element is not None
    print("打印模板的启停状态切换验证通过")
    #模板默认标签验证
    #设置默认
    ActionChains(driver).move_to_element(more).perform()
    driver.find_element(By.XPATH, '//*[@fieldid="iprint_default-btn"]').click()
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[text()="复制_状态验证"]/../..//*[text()="默认"]')))
    element = driver.find_elements(By.XPATH, '//*[text()="复制_状态验证"]/../..//*[text()="默认"]')
    assert element is not None
    #取消默认设置
    time.sleep(3)
    ActionChains(driver).move_to_element(more).perform()
    driver.find_element(By.XPATH, '//*[@fieldid="iprint_cancel_default-btn"]').click()
    WebDriverWait(driver, 20).until_not(EC.presence_of_element_located((By.XPATH, '//*[text()="复制_状态验证"]/../..//*[text()="默认"]')))
    element = driver.find_elements(By.XPATH, '//*[text()="复制_状态验证"]/../..//*[text()="默认"]')
    assert len(element) == 0
    print("打印模板的默认标签配置取消验证通过")
    #执行打印模板的删除操作
    ActionChains(driver).move_to_element(more).perform()
    driver.find_element(By.XPATH, '//*[@fieldid="iprint_delete-btn"][text()="删除"]').click()
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@fieldid="iprint_app_model_modal_title"]')))
    driver.find_element(By.XPATH, '//*[@fieldid="iprint_app_model_modal_footer_ok"]').click()
    WebDriverWait(driver, 20).until_not(EC.presence_of_element_located((By.XPATH, '//*[text()="复制_状态验证"]')))
    tem_element = driver.find_elements(By.XPATH, '//*[text()="复制_状态验证"]')
    assert len(tem_element) == 0
    print("新增打印模板删除完成")

def test_design_properties_default_value(login):
    '''
    这条用例仅作打印模板模板属性默认值检查
    '''
    driver = login
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@class="card_name"][text()="生产订单"]')))
    driver.find_element(By.XPATH, '//*[text()="生产订单"]/..//*[@fieldid="iprint_copy-btn"]').click()
    # 获取当前窗口句柄
    printlist_handle = driver.current_window_handle
    # 修改复制模板名称并确定
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
    # 返回打印模板浏览器页面
    WebDriverWait(driver, 20).until(lambda a: len(a.window_handles) > 1)
    for handle in driver.window_handles:
        if handle != printlist_handle:
            driver.switch_to.window(handle)
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="set-propty"]')))
    driver.find_element(By.XPATH,'//*[@id="set-propty"]').click()
    #验证模板编码框不可编辑
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@fieldid="design|InputText|tenantPageCode|Input"]')))
    element = driver.find_element(By.XPATH,'//*[@fieldid="design|InputText|tenantPageCode|Input"]')
    assert not element.is_enabled()
    #验证模板名称与新增该模板配置的名称一致
    element = driver.find_element(By.XPATH,'//*[@fieldid="design|InputText|uititle|Input"]')
    assert element.get_attribute("value") == "复制_模板属性验证"
    #验证横向矩阵默认值为1
    element = driver.find_element(By.XPATH,'//*[@fieldid="design|InputNumber|MergePrintPagesX|InputNumber"]')
    assert element.get_attribute("value") == "1"
    #验证总想矩阵默认值为1
    element = driver.find_element(By.XPATH, '//*[@fieldid="design|InputNumber|MergePrintPagesY|InputNumber"]')
    assert element.get_attribute("value") == "1"
    #验证循环主体为【暂无】
    element = driver.find_element(By.XPATH,'//*[@fieldid="design|InputSelect|mainTable|Select_search_input"]')
    assert element.get_attribute("value") == "暂无"
    #验证多页面打印方式默认值为【按单据】
    element = driver.find_element(By.XPATH, '//*[@fieldid="design|InputSelect|pageTemplateCircle|Select_search_input"]')
    assert element.get_attribute("value") == "按模板页面"
    #下边这几个验证项是检查属性按钮开关状态的
    #单据间隔打印默认关闭
    element = driver.find_element(By.XPATH,'//*[@fieldid="design|InputBool|intervalPrinting|Switch"]')
    assert 'checked' not in element.get_attribute("class")
    #双面打印默认关闭
    element = driver.find_element(By.XPATH, '//*[@fieldid="design|InputBool|duplexPrinting|Switch"]')
    assert 'checked' not in element.get_attribute("class")
    #仅打印有效审批意见默认关闭
    element = driver.find_element(By.XPATH, '//*[@fieldid="design|InputBool|noPrintReverse|Switch"]')
    assert 'checked' not in element.get_attribute("class")
    #不打印无效抢占审批默认关闭
    element = driver.find_element(By.XPATH, '//*[@fieldid="design|InputBool|excludeGrab|Switch"]')
    assert 'checked' not in element.get_attribute("class")
    #不打印自动跳过审批默认关闭
    element = driver.find_element(By.XPATH, '//*[@fieldid="design|InputBool|excludeNoUserCompleteAuto|Switch"]')
    assert 'checked' not in element.get_attribute("class")
    print("打印模板设计器模板属性默认值验证通过")
    driver.close()
    driver.switch_to.window(printlist_handle)
    more = driver.find_element(By.XPATH, '//*[text()="复制_模板属性验证"]/../..//*[@fieldid="iprint_more-btn"]')
    # 执行打印模板的删除操作
    ActionChains(driver).move_to_element(more).perform()
    driver.find_element(By.XPATH, '//*[@fieldid="iprint_delete-btn"][text()="删除"]').click()
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@fieldid="iprint_app_model_modal_title"]')))
    driver.find_element(By.XPATH, '//*[@fieldid="iprint_app_model_modal_footer_ok"]').click()
    WebDriverWait(driver, 20).until_not(EC.presence_of_element_located((By.XPATH, '//*[text()="复制_模板属性验证"]')))
    tem_element = driver.find_elements(By.XPATH, '//*[text()="复制_模板属性验证"]')
    assert len(tem_element) == 0
    print("新增打印模板删除完成")
def test_kongjian_list_drag_default_value(login):
    '''
    该用例用于进行打印模板设计器中列表控件的删除、新增、配置后的默认属性验证
    '''
    driver = login
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@class="card_name"][text()="生产订单"]')))
    driver.find_element(By.XPATH, '//*[text()="生产订单"]/..//*[@fieldid="iprint_copy-btn"]').click()
    # 获取当前窗口句柄
    printlist_handle = driver.current_window_handle
    # 修改复制模板名称并确定
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
    # 返回打印模板浏览器页面
    WebDriverWait(driver, 20).until(lambda a: len(a.window_handles) > 1)
    for handle in driver.window_handles:
        if handle != printlist_handle:
            driver.switch_to.window(handle)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="set-propty"]')))
    #开始进行列表控件的新增、验证过程
    #等待并删除画布上已经配置好的列表控件
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'//*[@title="列表: 生产订单表体"]')))
    element = driver.find_element(By.XPATH,'//*[@title="列表: 生产订单表体"]')
    if element:
        element.click()
        #等待删除按钮出现并点击
        WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'//*[@title="列表: 生产订单表体"]/..//*[contains(@class,"delete-button")]')))
        driver.find_element(By.XPATH,'//*[@title="列表: 生产订单表体"]/..//*[contains(@class,"delete-button")]').click()
        element = driver.find_elements(By.XPATH, '//*[@title="列表: 生产订单表体"]')
        assert len(element) ==0
        print("系统预置的列表在画布删除成功")
    #通过拖拽添加新列表控件并进行元素配置
    #配置列表控件element
    list_element = driver.find_element(By.XPATH,'//*[@fieldid="design|ComponentGroup|Panel|tableGroup|table"]')
    print("获取到列表控件")
    #配置画布目标element
    targ_element = driver.find_element(By.XPATH,'//*[@id="watermarkWordCover"]')
    print("获取到画布")
    #将列表控件移动到目标位置
    #ActionChains(driver).drag_and_drop(list_element,targ_element).perform()
    action = ActionChains(driver)
    action.move_to_element(list_element).perform()
    action.click_and_hold()
    # 3. 将鼠标移动到画布的中心位置
    # 计算画布中心坐标
    print("x坐标是"+str(targ_element.location['x']))
    print("y坐标是"+str(targ_element.location['y']))
    canvas_center_x = targ_element.location['x'] + 200
    canvas_center_y = targ_element.location['y'] + 250
    action.move_by_offset(canvas_center_x - list_element.location['x'],
                           canvas_center_y - list_element.location['y']).perform()
    action.release().perform()
    print("列表控件完成向画布拖入操作")
    #验证列表设置弹窗弹出正常
    WebDriverWait(driver,20).until(EC.presence_of_element_located((By.XPATH,'//*[@id="inputDesignModalHeader"]')))
    list_settings_element = driver.find_element(By.XPATH,'//*[@id="inputDesignModalHeader"]')
    assert list_settings_element is not None

    #搜索选择字段

    #点击确定保存列表

    #检查列表配置后在画布上展示正常

    #点击并检查列表的各默认属性值是否正常